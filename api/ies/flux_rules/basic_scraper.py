"""Scraper de exploración del board de Miró (solo lectura).

Baja el board completo vía la API REST v2 de Miró y lo vuelca a JSON
para descifrar las convenciones visuales (qué shape/estilo/color usa cada
tipo de pieza: mensaje, botones, lista, bifurcación, frame, etc.).

Variables hardcodeadas a propósito: este script es un insumo puntual para
construir el JSON de ejemplo, no parte del producto. Usa solo la librería
estándar (urllib) para no requerir instalar dependencias.
"""

import json
import urllib.parse
import urllib.request
import urllib.error
from collections import defaultdict
from pathlib import Path

# --- Configuración (hardcodeada a propósito) -------------------------
ACCESS_TOKEN = "eyJtaXJvLm9yaWdpbiI6ImV1MDEifQ_iE_XXyAtX2ONg_AlhzviAvnJte0"
BOARD_ID = "uXjVHIWwkig="

BASE_URL = f"https://api.miro.com/v2/boards/{BOARD_ID}"
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Accept": "application/json",
}
OUT_DIR = Path(__file__).parent


def api_get(path: str, params: dict | None = None) -> dict:
    """GET a un endpoint del board y devuelve el JSON parseado."""
    url = f"{BASE_URL}{path}"
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        raise SystemExit(
            f"HTTP {exc.code} en {path}: {body}"
        ) from exc


def get_all(path: str) -> list[dict]:
    """Pagina por `cursor` hasta agotar y devuelve todos los `data`."""
    items: list[dict] = []
    params: dict = {"limit": 50}
    while True:
        page = api_get(path, params)
        items.extend(page.get("data", []))
        cursor = page.get("cursor")
        if not cursor:
            break
        params["cursor"] = cursor
    return items


def organize(items: list[dict], connectors: list[dict]) -> dict:
    """Agrupa los ítems hijos bajo su frame; el resto quedan huérfanos.

    El endpoint genérico /items ya devuelve frames e hijos mezclados;
    cada hijo trae `parent.id`. Reconstruimos la jerarquía localmente.
    """
    frames = [it for it in items if it.get("type") == "frame"]
    children = [it for it in items if it.get("type") != "frame"]

    by_parent: dict[str, list[dict]] = defaultdict(list)
    orphans: list[dict] = []
    for it in children:
        parent_id = (it.get("parent") or {}).get("id")
        if parent_id:
            by_parent[parent_id].append(it)
        else:
            orphans.append(it)

    frames_out = []
    for fr in frames:
        frames_out.append({
            "id": fr.get("id"),
            "title": fr.get("data", {}).get("title"),
            "style": fr.get("style"),
            "position": fr.get("position"),
            "geometry": fr.get("geometry"),
            "items": by_parent.get(fr.get("id"), []),
        })

    return {
        "board_id": BOARD_ID,
        "counts": {
            "frames": len(frames),
            "items_total": len(items),
            "children": len(children),
            "orphans": len(orphans),
            "connectors": len(connectors),
        },
        "frames": frames_out,
        "orphan_items": orphans,
        "connectors": connectors,
    }


def main() -> None:
    print("Bajando ítems...")
    items = get_all("/items")
    print(f"  {len(items)} ítems")

    print("Bajando conectores...")
    connectors = get_all("/connectors")
    print(f"  {len(connectors)} conectores")

    raw = {"items": items, "connectors": connectors}
    (OUT_DIR / "board_raw.json").write_text(
        json.dumps(raw, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    organized = organize(items, connectors)
    (OUT_DIR / "board_organized.json").write_text(
        json.dumps(organized, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("\nResumen:")
    for key, val in organized["counts"].items():
        print(f"  {key}: {val}")
    print("\nFrames encontrados:")
    for fr in organized["frames"]:
        n = len(fr["items"])
        print(f"  - {fr['title']!r} ({n} ítems)  id={fr['id']}")
    print("\nEscrito: board_raw.json, board_organized.json")


if __name__ == "__main__":
    main()