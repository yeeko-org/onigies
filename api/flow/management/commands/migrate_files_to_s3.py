"""Migra los archivos subidos entre el disco local y S3, en ambos sentidos.

S3 es un puente temporal: el bucket privado `onigies-v3-temporal` sostiene
los archivos mientras llega el servidor de la UNAM, dentro de unos dos
meses. Por eso el comando es bidireccional — la fase de bajada no es un
rollback, es la mudanza que ya está prevista.

Fases de uso (en el servidor, una vez cada una):

    python manage.py migrate_files_to_s3 --dry-run   # censo previo
    python manage.py migrate_files_to_s3             # subida real
    # ...ahora sí, USE_S3_FILES=1 y reinicio del servicio...
    python manage.py migrate_files_to_s3 --verify    # BD vs S3

La subida corre con el flag TODAVÍA APAGADO: instancia el backend S3
directamente, ignorando USE_S3_FILES, para copiar todo antes de encender
el switch y no abrir una ventana de 404s.

Fase inversa, cuando toque mudarse al servidor de la UNAM:

    python manage.py migrate_files_to_s3 --download --dry-run
    python manage.py migrate_files_to_s3 --download  # S3 -> MEDIA_ROOT
    # ...apagar USE_S3_FILES y reiniciar...

La fuente de verdad es la BD, no el disco: los nombres salen de
flow.Attachment, ies.Institution.logo y example.Evidence. Los archivos
sueltos en disco sin registro se reportan como huérfanos, pero nunca se
suben. En ningún sentido se borra nada.
"""
import json
import os
from typing import Any, Optional

from django.conf import settings
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.core.management.base import BaseCommand, CommandError
from storages.backends.s3 import S3Storage

from example.models import Evidence
from flow.models import Attachment
from ies.models import Institution

# Carpetas de MEDIA_ROOT donde viven los archivos subidos (ver
# flow/upload_paths.py y los upload_to de Institution y Evidence).
MEDIA_PREFIXES = ("attachments", "evidences", "ies")


def s3_setting(name: str, default: Optional[str] = None) -> Optional[str]:
    """Valor de settings si existe; si no, del entorno.

    El bloque S3 de settings solo se evalúa con USE_S3_FILES encendido,
    y este comando corre justamente con el flag apagado.
    """
    value = getattr(settings, name, None)
    return value if value else os.getenv(name, default)


def get_media_root() -> str:
    """Raíz del disco local, también con el flag encendido.

    El fallback cubre los despliegues que aún no tienen el MEDIA_ROOT
    incondicional de settings; la fase de bajada lo necesita mientras el
    flag sigue activo.
    """
    media_root = getattr(settings, "MEDIA_ROOT", None)
    return media_root or os.path.join(settings.BASE_DIR, "files")


def build_s3_storage() -> S3Storage:
    bucket = s3_setting("AWS_STORAGE_BUCKET_NAME")
    if not bucket:
        raise CommandError(
            "Falta AWS_STORAGE_BUCKET_NAME (settings o entorno)")
    # Sin región no hay firma válida; adivinarla mandaría los archivos
    # al bucket equivocado o al endpoint global.
    region = s3_setting("AWS_S3_REGION_NAME")
    if not region:
        raise CommandError(
            "Falta AWS_S3_REGION_NAME (settings o entorno)")
    return S3Storage(
        bucket_name=bucket,
        region_name=region,
        location=s3_setting("AWS_LOCATION", "files"),
        # Explícitas para no caer en silencio al perfil de la instancia
        # EC2 si el .env viene mal.
        access_key=os.getenv("AWS_ACCESS_KEY_ID"),
        secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        # El bucket tiene las ACL deshabilitadas.
        default_acl=None,
        querystring_auth=False,
        # la migración replica keys exactas, sin sufijos anti-colisión
        file_overwrite=True,
    )


def list_s3_sizes(storage: S3Storage) -> dict[str, int]:
    """Mapa name -> tamaño de todo lo que ya está bajo AWS_LOCATION.

    Un solo listado paginado en vez de un HEAD por archivo: unas pocas
    peticiones para todo el bucket.
    """
    client = storage.connection.meta.client
    prefix = f'{s3_setting("AWS_LOCATION", "files")}/'
    sizes: dict[str, int] = {}
    paginator = client.get_paginator("list_objects_v2")
    pages = paginator.paginate(
        Bucket=s3_setting("AWS_STORAGE_BUCKET_NAME"), Prefix=prefix)
    for page in pages:
        for obj in page.get("Contents", []):
            sizes[obj["Key"][len(prefix):]] = obj["Size"]
    return sizes


class Command(BaseCommand):
    help = (
        "Copia los archivos de Attachment, Institution.logo y Evidence "
        "entre el disco y S3. Idempotente; --verify solo compara BD vs "
        "S3 y --download hace el camino inverso."
    )

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--dry-run", action="store_true",
            help="Solo reporta qué copiaría, sin escribir nada")
        parser.add_argument(
            "--verify", action="store_true",
            help="Solo verifica existencia y tamaño en S3 de cada "
                 "archivo registrado en BD")
        parser.add_argument(
            "--download", action="store_true",
            help="Sentido inverso: baja de S3 al disco (MEDIA_ROOT), "
                 "para la mudanza al servidor de la UNAM")
        parser.add_argument(
            "--limit", type=int, default=None,
            help="Procesa solo los primeros N archivos (pruebas)")
        parser.add_argument(
            "--report", default="migrate_s3_report.json",
            help="Ruta del JSON con el detalle por archivo")

    def handle(self, *args, **options) -> None:
        self.media_root = get_media_root()
        self.local_storage = FileSystemStorage(location=self.media_root)
        storage = self.safe_build_storage(options)

        all_names = self.get_db_file_names()
        names = all_names[:options["limit"]] if options["limit"] \
            else all_names
        s3_sizes, s3_error = self.safe_list_s3(storage, options)
        self.stdout.write(
            f"{len(all_names)} archivos en BD | "
            f"{len(s3_sizes)} objetos ya en S3")

        results: dict[str, list] = {
            "uploaded": [], "downloaded": [], "skipped": [],
            "missing_local": [], "missing_s3": [], "size_mismatch": [],
            "failed": [],
        }
        for idx, name in enumerate(names, start=1):
            self.process_one(name, storage, s3_sizes, options, results)
            if idx % 500 == 0:
                self.stdout.write(f"... {idx}/{len(names)}")

        # los huérfanos se detectan contra la BD completa, aunque se
        # procese un subconjunto con --limit
        results["orphans"] = self.find_orphans(set(all_names))
        self.write_report(results, options, s3_error)

    def safe_build_storage(self, options: dict) -> Optional[S3Storage]:
        """Backend S3, opcional en --dry-run.

        El censo previo se corre en local, donde ni siquiera hay bucket
        configurado; ahí basta con contar el lado del disco.
        """
        try:
            return build_s3_storage()
        except CommandError:
            if not options["dry_run"]:
                raise
            return None

    def safe_list_s3(
            self, storage: Optional[S3Storage], options: dict,
    ) -> tuple[dict[str, int], Optional[str]]:
        """Listado del bucket, tolerante solo en --dry-run.

        El censo previo se corre en local, sin credenciales de AWS: ahí
        el listado inaccesible se reporta, no aborta. En cualquier modo
        que escriba o verifique, no poder listar sí es un error.
        """
        try:
            if storage is None:
                raise CommandError("bucket S3 sin configurar")
            return list_s3_sizes(storage), None
        except Exception as exc:
            if not options["dry_run"]:
                raise CommandError(f"No se pudo listar el bucket: {exc}")
            self.stdout.write(self.style.WARNING(
                f"Listado de S3 no disponible: {exc}"))
            return {}, str(exc)

    def get_db_file_names(self) -> list[str]:
        attachment_names = Attachment.objects.exclude(file="") \
            .values_list("file", flat=True)
        logo_names = Institution.objects.exclude(logo="") \
            .values_list("logo", flat=True)
        evidence_names = Evidence.objects.exclude(file="") \
            .values_list("file", flat=True)
        # dict.fromkeys: dedup preservando orden. Los Attachment
        # espejados apuntan a los mismos nombres que los Evidence viejos.
        return list(dict.fromkeys(
            list(attachment_names) + list(logo_names)
            + list(evidence_names)))

    def process_one(
            self, name: str, storage: Optional[S3Storage],
            s3_sizes: dict[str, int], options: dict,
            results: dict[str, list],
    ) -> None:
        local_path = os.path.join(self.media_root, name)
        local_size = os.path.getsize(local_path) \
            if os.path.exists(local_path) else None
        s3_size = s3_sizes.get(name)

        if options["verify"]:
            self.verify_one(name, local_size, s3_size, results)
        elif options["download"]:
            self.download_one(
                name, local_size, s3_size, storage, options, results)
        else:
            self.upload_one(
                name, local_path, local_size, s3_size, storage, options,
                results)

    def verify_one(
            self, name: str, local_size: Optional[int],
            s3_size: Optional[int], results: dict[str, list],
    ) -> None:
        if s3_size is None:
            results["missing_s3"].append(name)
        elif local_size is not None and local_size != s3_size:
            results["size_mismatch"].append(
                {"name": name, "local": local_size, "s3": s3_size})
        else:
            results["skipped"].append(name)

    def upload_one(
            self, name: str, local_path: str, local_size: Optional[int],
            s3_size: Optional[int], storage: S3Storage, options: dict,
            results: dict[str, list],
    ) -> None:
        if local_size is None:
            results["missing_local"].append(name)
            return
        if s3_size == local_size:
            results["skipped"].append(name)
            return
        if options["dry_run"]:
            results["uploaded"].append(name)
            return
        try:
            with open(local_path, "rb") as fh:
                storage.save(name, File(fh))
            results["uploaded"].append(name)
        except Exception as exc:
            results["failed"].append({"name": name, "error": str(exc)})

    def download_one(
            self, name: str, local_size: Optional[int],
            s3_size: Optional[int], storage: S3Storage, options: dict,
            results: dict[str, list],
    ) -> None:
        """Baja un archivo de S3 al disco, con las mismas reglas.

        Un archivo local del mismo tamaño se salta; uno de tamaño
        distinto se reporta como discrepancia y se deja intacto, porque
        aquí nunca se borra ni se pisa nada.
        """
        if s3_size is None:
            results["missing_s3"].append(name)
            return
        if local_size == s3_size:
            results["skipped"].append(name)
            return
        if local_size is not None:
            results["size_mismatch"].append(
                {"name": name, "local": local_size, "s3": s3_size})
            return
        if options["dry_run"]:
            results["downloaded"].append(name)
            return
        try:
            with storage.open(name, "rb") as fh:
                self.local_storage.save(name, File(fh))
            results["downloaded"].append(name)
        except Exception as exc:
            results["failed"].append({"name": name, "error": str(exc)})

    def find_orphans(self, known: set[str]) -> list[str]:
        """Archivos en disco bajo las carpetas de subida sin registro en
        BD. Informativo: no se suben ni se borran."""
        orphans = []
        for prefix in MEDIA_PREFIXES:
            root = os.path.join(self.media_root, prefix)
            for dirpath, _dirs, files in os.walk(root):
                for fname in files:
                    full = os.path.join(dirpath, fname)
                    rel = os.path.relpath(full, self.media_root)
                    rel = rel.replace(os.sep, "/")
                    if rel not in known:
                        orphans.append(rel)
        return orphans

    def write_report(
            self, results: dict[str, list], options: dict,
            s3_error: Optional[str],
    ) -> None:
        mode = self.get_mode(options)
        summary = {key: len(values) for key, values in results.items()}
        payload: dict[str, Any] = {
            "mode": mode, "summary": summary, "detail": results}
        if s3_error:
            payload["s3_listing_error"] = s3_error
        with open(options["report"], "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
        self.stdout.write(self.style.SUCCESS(
            f"[{mode}] " + " | ".join(
                f"{key}: {count}" for key, count in summary.items())))
        self.stdout.write(f"Detalle en {options['report']}")

    def get_mode(self, options: dict) -> str:
        if options["verify"]:
            return "verify"
        base = "download" if options["download"] else "upload"
        return f"{base}-dry-run" if options["dry_run"] else base
