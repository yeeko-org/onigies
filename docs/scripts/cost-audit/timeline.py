"""Bloques de actividad por umbral de hueco, para calibrar. No valúa: es la
sonda que muestra cuánto cambia el total según dónde se corte el hueco.

Uso:  python3 timeline.py [--from ISO] [--to ISO] [--gaps 10,20,30,45]
"""
import datetime
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import credit as C

ARGS = sys.argv[1:]
ROOT, ROOTS, BASE, AUDIT = C.resolve_config(ARGS)
A = C.parse_local(C.arg_of(ARGS, "--from") or "") if C.arg_of(ARGS, "--from") else None
B = C.parse_local(C.arg_of(ARGS, "--to") or "") if C.arg_of(ARGS, "--to") else None
GAPS = [int(x) for x in (C.arg_of(ARGS, "--gaps") or "10,20,30,45").split(",")]

events = []
for p in glob.glob(BASE + "/**/*.jsonl", recursive=True):
    if any(f in p for f in AUDIT):
        continue
    sid = os.path.basename(p)[:-6]
    for line in open(p, errors="replace"):
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except Exception:
            continue
        t = C.parse_ts(d.get("timestamp")) if d.get("timestamp") else None
        if t and (not A or t >= A) and (not B or t <= B):
            events.append((t, sid))
events.sort()
if not events:
    print("sin eventos en la ventana")
    raise SystemExit

print("proyecto:", ROOT)
print("eventos:", len(events),
      "rango:", C.local(events[0][0]).strftime("%Y-%m-%d %H:%M"),
      "->", C.local(events[-1][0]).strftime("%Y-%m-%d %H:%M"))


def blocks(evs, gap):
    out = []
    cur = [evs[0]]
    for e in evs[1:]:
        if (e[0] - cur[-1][0]).total_seconds() / 60 <= gap:
            cur.append(e)
        else:
            out.append(cur)
            cur = [e]
    out.append(cur)
    return out


line = ["TOTAL"]
for gap in GAPS:
    bl = blocks(events, gap)
    h = sum((x[-1][0] - x[0][0]).total_seconds() for x in bl) / 3600
    line.append("g%d=%.1fh(%db)" % (gap, h, len(bl)))
print("  ".join(line))
