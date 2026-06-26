#!/usr/bin/env bash
#
# Despliegue: production (40ce63b) -> main  —  migración StatusControl -> flow.Status
# ---------------------------------------------------------------------------
# Lleva el backend del commit de producción al último de main. Todo el cambio
# es ADITIVO (coexistencia): la fase de borrado §8 del plan NO está en main,
# así que ningún dato viejo se toca. Doc de referencia:
#   api/ies/flux_rules/PLAN_flujo_validacion.md  (§6 mapeo, §9 secuencia)
#
# USO  (siempre desde el directorio api/, con el venv del proyecto):
#   1) ENSAYO sobre el clon local (schema public):   ./deploy_flow_migration.sh local
#   2) PRODUCCIÓN, idéntico, tras validar el ensayo:  ./deploy_flow_migration.sh prod
#
# EN EL SERVER, ANTES de correr este script en modo prod (así es como el script
# llega al server; bash no debe pull-ear su propio archivo en ejecución):
#   git pull origin production      # production ya fast-forwardeada a main
#
# Todos los comandos de datos (seed_flow, resave_institutions, migrate_flow_data,
# verify_flow_data, migrate_ps_schemas) son IDEMPOTENTES: re-ejecutarlos es seguro.
#
# Antes de correr en prod, edita el BLOQUE DE CONFIGURACIÓN de abajo.
# ---------------------------------------------------------------------------

set -euo pipefail

# ----------------------------- CONFIGURACIÓN -------------------------------
# Python del venv. Si ya activaste el venv, "python" basta. Si no, pon la ruta:
#   export PYTHON=/ruta/al/venv/bin/python   (o edítalo aquí)
PYTHON="${PYTHON:-python}"

# Las credenciales de la BD para el pg_dump se leen de api/.env más abajo
# (las mismas que usa Django); no dependen del entorno del shell.

# Solo se usan cuando MODE=prod:
GIT_BRANCH="production"             # rama desplegada (fast-forwardeada a main)
SUPERVISOR_PROGRAM="apionigies"     # supervisorctl {stop,start} <programa>

# Comandos para detener/levantar el API en la ventana de mantenimiento.
# Ajústalos a tu server: si supervisord corre como root, antepón sudo; si usa
# otro socket: "sudo supervisorctl -c /etc/supervisor/supervisord.conf stop ...".
# SKIP_SERVICE=1 omite el control del servicio (lo bajas/levantas tú a mano).
SERVICE_STOP="${SERVICE_STOP:-sudo supervisorctl stop $SUPERVISOR_PROGRAM}"
SERVICE_START="${SERVICE_START:-sudo supervisorctl start $SUPERVISOR_PROGRAM}"

# Carpeta donde cae el respaldo de seguridad.
BACKUP_DIR="${BACKUP_DIR:-./_backups}"
# ---------------------------------------------------------------------------

MODE="${1:-}"
if [[ "$MODE" != "local" && "$MODE" != "prod" ]]; then
  echo "Uso: $0 [local|prod]" >&2
  exit 2
fi

# Se ejecuta siempre desde donde vive manage.py.
cd "$(dirname "$0")"

# Pausa de inspección entre fases. En prod podés correr el script entero o
# fase por fase; cada gate te deja leer la salida antes de seguir.
gate() {
  echo
  read -r -p ">>> $1  [Enter para continuar / Ctrl-C para abortar] "
}

# Credenciales de la BD leídas de api/.env vía python-dotenv (cwd ya es api/).
# Igual que Django con load_dotenv(); el password nunca se imprime.
read_env() { $PYTHON -c "from dotenv import dotenv_values as d; print(d('.env').get('$1',''))"; }
DB_NAME="$(read_env DATABASE_NAME)"
DB_USER="$(read_env DATABASE_USER)"
DB_HOST="$(read_env DATABASE_HOST)"
DB_PORT="$(read_env DATABASE_PORT)"
export PGPASSWORD="$(read_env DATABASE_PASSWORD)"

echo "==========================================================="
echo " ONIGIES — migración a flow.Status   (MODE=$MODE)"
echo " DB=$DB_NAME  USER=$DB_USER  HOST=$DB_HOST"
echo "==========================================================="

# ---------------------------------------------------------------------------
# FASE 0 — Respaldo de seguridad (red de rescate; restaurar si algo truena)
# ---------------------------------------------------------------------------
# SKIP_BACKUP=1 omite el pg_dump (úsalo cuando ya tomaste un snapshot de RDS,
# que es el respaldo nativo y a prueba de versiones para una BD en RDS).
if [[ "${SKIP_BACKUP:-0}" == "1" ]]; then
  echo "[FASE 0] pg_dump OMITIDO (SKIP_BACKUP=1)."
  echo "   Confirma que ya tienes un snapshot de RDS de '$DB_NAME' antes de seguir."
  gate "¿Snapshot de RDS tomado? Sigue: bajar servicio + migraciones."
else
  mkdir -p "$BACKUP_DIR"
  STAMP="$(date +%Y%m%d_%H%M%S)"
  BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_pre_flow_${STAMP}.dump"
  echo
  echo "[FASE 0] Respaldo -> $BACKUP_FILE"
  # Requiere pg_dump de versión >= la de RDS. -Fc = custom comprimido. BD completa.
  pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -Fc "$DB_NAME" -f "$BACKUP_FILE"
  echo "Respaldo OK ($(du -h "$BACKUP_FILE" | cut -f1))."
  echo "   Restauración (si hiciera falta):"
  echo "   PGPASSWORD=… pg_restore -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME --clean --if-exists $BACKUP_FILE"
  gate "Respaldo listo. Sigue: traer código + bajar servicio."
fi

# ---------------------------------------------------------------------------
# FASE 1 — Código + mantenimiento (solo prod; en local ya estás en main)
# ---------------------------------------------------------------------------
if [[ "$MODE" == "prod" ]]; then
  echo
  echo "[FASE 1] dependencias + mantenimiento"
  echo "   (el 'git pull origin $GIT_BRANCH' ya lo corriste a mano: es como"
  echo "    llegó este script al server)."
  # requirements no cambió entre los dos commits; se corre por seguridad.
  $PYTHON -m pip install -r requirements.txt

  if [[ "${SKIP_SERVICE:-0}" == "1" ]]; then
    echo "Control de servicio OMITIDO (SKIP_SERVICE=1): baja el API tú a mano."
    gate "¿API detenido? Sigue: migraciones de esquema."
  else
    echo "Bajando el servicio (ventana de mantenimiento): $SERVICE_STOP"
    eval "$SERVICE_STOP"
    gate "Servicio abajo. Sigue: migraciones de esquema."
  fi
fi

# ---------------------------------------------------------------------------
# FASE 2 — Migraciones de esquema
# ---------------------------------------------------------------------------
# El esquema se aplica en DOS tramos con seed_flow en medio (validado en el
# ensayo). Por qué: example.0008 agrega GoodPractice.status con default='bp_draft'
# (FK a flow_status) y la tabla de buenas prácticas TIENE filas; un migrate de
# un jalón intenta escribir bp_draft antes de que el seed lo cree -> FK violation.
# Tramo 1 = catálogo (flow) + survey (crea el ContentType de GeneralPackage que
# el seed necesita). El RunPython de answer/0003 (backfill axis_value -> NOT NULL)
# va en el tramo 2; en el ensayo pasó sobre 244 AxisValue sin orfandad.
echo
echo "[FASE 2] Estado actual de migraciones:"
$PYTHON manage.py showmigrations flow answer survey example ies ps_schema
echo
echo "Plan completo a aplicar (referencia; se hará en dos tramos):"
$PYTHON manage.py migrate --plan
gate "Revisa el plan. Sigue: esquema tramo 1 (catálogo)."

$PYTHON manage.py migrate flow      # tabla Status completa (0001-0006)
$PYTHON manage.py migrate survey    # ContentType de GeneralPackage (lo pide el seed)
echo "Esquema tramo 1 (catálogo) aplicado."
gate "Sigue: SEMBRAR el catálogo ANTES del resto del esquema."

# ---------------------------------------------------------------------------
# FASE 3 — Sembrado de catálogos (idempotente)
# ---------------------------------------------------------------------------
echo
echo "[FASE 3a] seed_flow — siembra los 32 Status (bp/cp/gen). CRÍTICO: va ANTES"
echo "          del resto del migrate para que example.0008 halle bp_draft."
$PYTHON manage.py seed_flow

echo
echo "[FASE 3b] migrate — resto del esquema: answer, example.0008, ies, ps_schema"
$PYTHON manage.py migrate

echo
echo "[FASE 3c] migrate_ps_schemas — recarga colecciones del dashboard"
$PYTHON manage.py migrate_ps_schemas
gate "Esquema completo + catálogos. Sigue: backfill de estructuras eager."

# ---------------------------------------------------------------------------
# FASE 4 — Backfill de estructuras eager (idempotente)
# ---------------------------------------------------------------------------
# Re-guarda cada Institution: crea GeneralPackage y pone defaults de status en
# objetos nuevos. Requiere seed_flow ya corrido (status_id es FK PROTECT).
echo
echo "[FASE 4] resave_institutions"
$PYTHON manage.py resave_institutions
gate "Estructuras backfilleadas. Sigue: migración de datos del flujo."

# ---------------------------------------------------------------------------
# FASE 5 — Migración de datos StatusControl -> flow.Status (idempotente)
# ---------------------------------------------------------------------------
# Copia status_register/status_sending -> status nuevo, comentarios -> FlowEvent
# y adjuntos -> Attachment. comments-user = primer superusuario (default).
# OJO (riesgo gen): si imprime "id viejo sin mapeo" para GeneralGroupResponse,
# es el desfase GEN_MAP vs seed; en el ensayo NO apareció (0 generales en
# producción). Si aparece, abortar y alinear GEN_MAP antes de continuar.
echo
echo "[FASE 5] migrate_flow_data"
$PYTHON manage.py migrate_flow_data
gate "Datos migrados. Sigue: VERIFICACIÓN (lee con calma)."

# ---------------------------------------------------------------------------
# FASE 6 — Verificación (solo lectura; el checkpoint del plan §9.4)
# ---------------------------------------------------------------------------
echo
echo "[FASE 6] verify_flow_data — conteos viejo vs nuevo"
$PYTHON manage.py verify_flow_data
echo
echo "REVISA: cada modelo debe decir [ok]. 'SIN MAPEO' o 'REVISAR' = parar."
gate "¿Conteos correctos? Sigue: levantar el servicio."

# ---------------------------------------------------------------------------
# FASE 7 — Levantar servicio (solo prod) + smoke test manual
# ---------------------------------------------------------------------------
if [[ "$MODE" == "prod" ]]; then
  echo
  echo "[FASE 7] Levantando el servicio…"
  if [[ "${SKIP_SERVICE:-0}" == "1" ]]; then
    echo "Control de servicio OMITIDO (SKIP_SERVICE=1): levanta el API tú a mano."
  else
    echo "$SERVICE_START"
    eval "$SERVICE_START"
  fi
  echo
  echo "Smoke test sugerido:"
  echo "  - GET https://apionigies.yeeko.org/api/  (responde)"
  echo "  - Login en el dashboard + abrir /respuestas y /dashboard"
  echo "  - Abrir un Envío de Buenas Prácticas y ver su status nuevo"
fi

echo
echo "==========================================================="
echo " LISTO ($MODE). Respaldo en: $BACKUP_FILE"
echo "==========================================================="