"""Análisis estructurado de los frames del board de Miró.

Lee board_organized.json (generado por basic_scraper.py) e interpreta el
flujo de status según las convenciones visuales del dueño del board.
No toca la red: solo procesa el JSON ya descargado.

Salida: imprime un resumen legible y escribe analysis.json con el
modelo consolidado (statuses, transitions, parent_child_rules,
model_applicability) por frame.
"""

import json
import re
from pathlib import Path

OUT_DIR = Path(__file__).parent
ORG = json.loads((OUT_DIR / "board_organized.json").read_text("utf-8"))

# --- Convenciones de color (provistas por el dueño) ------------------
FILL_ROLE = {
    "#c6dcff": "ies",            # azul claro: mueve la IES
    "#dedaff": "revisora",       # morado claro: mueve la revisora
    "#fff6b6": "terminal",       # amarillo: inmóvil/terminal
}
STROKE_ROLE = {
    "#b0b0b0": "dependency",     # gris: regla padre-hijo (no transición)
    "#305bab": "ies",            # azul: transición IES
    "#e456da": "revisora",       # rosa: transición revisora
    "#6631d7": "revisora",       # morado: transición revisora
}
GRAY_FILL = "#e7e7e7"            # relleno gris en círculo = modelo NO aplica
# La leyenda distingue dos verdes de contorno:
GREEN_UP = "#2dc75c"             # recálculo hacia arriba (propaga al padre)
GREEN_DOWN = "#067429"           # recálculo hacia abajo
GREEN_BORDERS = {GREEN_UP, GREEN_DOWN}

# Letra de modelo -> nombre por frame
MODEL_NAMES = {
    "Cuestionario principal": {
        "A": "AxisValue",
        "O": "ObservableResponse",
        "G": "GroupResponse",
    },
    "Buenas prácticas": {
        "P": "GoodPracticePackage",
        "G": "GoodPractice",
    },
}


def strip_html(html: str | None) -> str:
    if not html:
        return ""
    txt = re.sub(r"<[^>]+>", " ", html)
    txt = txt.replace("&nbsp;", " ").replace("&amp;", "&")
    return re.sub(r"\s+", " ", txt).strip()


def center(it: dict) -> tuple[float, float]:
    p = it["position"]
    return p["x"], p["y"]


def is_letter_circle(it: dict) -> bool:
    if it["type"] != "shape":
        return False
    if it["data"].get("shape") != "circle":
        return False
    return len(strip_html(it["data"].get("content"))) <= 2


def analyze_frame(frame: dict) -> dict:
    title = frame["title"]
    models = MODEL_NAMES.get(title, {})
    items = frame["items"]
    shapes = [it for it in items if it["type"] == "shape"]

    circles = [it for it in shapes if is_letter_circle(it)]
    # status = rectángulo/round_rectangle con texto, fill conocido de rol
    statuses = []
    legend_box = None
    recalc_boxes = []
    for it in shapes:
        if is_letter_circle(it):
            continue
        content = strip_html(it["data"].get("content"))
        fill = it["style"].get("fillColor")
        bw = float(it["style"].get("borderWidth", "0"))
        shp = it["data"].get("shape")
        # caja de leyenda: sin texto, borde negro grueso
        if not content and bw >= 10:
            legend_box = it
            continue
        # cajas de leyenda "Recálculo hacia arriba/abajo"
        if content.startswith("Recálculo"):
            recalc_boxes.append(it)
            continue
        if fill in FILL_ROLE:
            statuses.append(it)

    # Excluir los círculos de la leyenda: están dentro/junto al legend_box
    # (los grandes w=68). Filtramos círculos cuyo centro cae dentro del
    # bounding box del legend_box.
    legend_circle_ids = set()
    if legend_box:
        lx, ly = center(legend_box)
        lw = legend_box["geometry"]["width"]
        lh = legend_box["geometry"]["height"]
        x0, x1 = lx - lw / 2, lx + lw / 2
        y0, y1 = ly - lh / 2, ly + lh / 2
        for c in circles:
            cx, cy = center(c)
            if x0 <= cx <= x1 and y0 <= cy <= y1:
                legend_circle_ids.add(c["id"])

    flow_circles = [c for c in circles if c["id"] not in legend_circle_ids]

    # Asociar cada círculo de flujo a su status más cercano (por centro).
    def nearest_status(circle):
        cx, cy = center(circle)
        best, bestd = None, 1e18
        for st in statuses:
            sx, sy = center(st)
            d = (cx - sx) ** 2 + (cy - sy) ** 2
            if d < bestd:
                bestd, best = d, st
        return best

    status_models: dict[str, dict[str, str]] = {
        st["id"]: {} for st in statuses
    }
    for c in flow_circles:
        st = nearest_status(c)
        if not st:
            continue
        letter = strip_html(c["data"].get("content")).upper()
        fill = c["style"].get("fillColor")
        applies = fill != GRAY_FILL
        status_models[st["id"]][letter] = "no" if not applies else "si"

    # Construir lista de status
    status_out = []
    name_by_id = {}
    for st in statuses:
        sid = st["id"]
        name = strip_html(st["data"].get("content"))
        name_by_id[sid] = name
        fill = st["style"].get("fillColor")
        border = st["style"].get("borderColor")
        shp = st["data"].get("shape")
        green = border in GREEN_BORDERS
        rounded = shp == "round_rectangle"
        recalc = None
        if green and rounded:
            recalc = "up" if border == GREEN_UP else "down"
        applic = status_models.get(sid, {})
        status_out.append({
            "id": sid,
            "name": name,
            "fill": fill,
            "role": FILL_ROLE.get(fill, "?"),
            "border_color": border,
            "shape": shp,
            "upward_propagation": recalc == "up",
            "recalc": recalc,
            "model_applicability": {
                models.get(k, k): v for k, v in sorted(applic.items())
            },
        })

    # Conectores cuyos dos extremos están en este frame
    frame_ids = {it["id"] for it in items}
    transitions = []
    dependencies = []
    for con in ORG["connectors"]:
        s = con.get("startItem", {}).get("id")
        e = con.get("endItem", {}).get("id")
        if s not in frame_ids or e not in frame_ids:
            continue
        color = con.get("style", {}).get("strokeColor")
        role = STROKE_ROLE.get(color, "?")
        rec = {
            "id": con["id"],
            "from_id": s,
            "from": name_by_id.get(s, f"<{s}>"),
            "to_id": e,
            "to": name_by_id.get(e, f"<{e}>"),
            "stroke": color,
        }
        if role == "dependency":
            dependencies.append(rec)
        else:
            rec["role"] = role
            transitions.append(rec)

    return {
        "frame": title,
        "models": [
            {"letter": k, "model": v} for k, v in models.items()
        ],
        "legend_box_id": legend_box["id"] if legend_box else None,
        "recalc_boxes": [
            {
                "text": strip_html(b["data"].get("content")),
                "border_color": b["style"].get("borderColor"),
                "rounded": b["data"].get("shape") == "round_rectangle",
            }
            for b in recalc_boxes
        ],
        "statuses": status_out,
        "transitions": transitions,
        "dependencies": dependencies,
    }


def main() -> None:
    result = {}
    for fr in ORG["frames"]:
        result[fr["title"]] = analyze_frame(fr)
    (OUT_DIR / "analysis.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False), "utf-8"
    )

    for title, data in result.items():
        print("=" * 72)
        print("FRAME:", title)
        print("Modelos:", data["models"])
        print("\nSTATUSES:")
        for s in data["statuses"]:
            prop = " [PROPAGA-ARRIBA]" if s["upward_propagation"] else ""
            print(f"  - {s['name']!r} role={s['role']}{prop}")
            print(f"      aplicabilidad: {s['model_applicability']}")
        print("\nTRANSICIONES (rosa/morado/azul):")
        for t in data["transitions"]:
            print(f"  {t['from']!r} -> {t['to']!r}  [{t['role']}]")
        print("\nDEPENDENCIAS (gris):")
        for d in data["dependencies"]:
            same = "  (AUTO)" if d["from_id"] == d["to_id"] else ""
            print(f"  {d['from']!r} <- hijos en {d['to']!r}{same}")
    print("\nEscrito: analysis.json")


if __name__ == "__main__":
    main()
