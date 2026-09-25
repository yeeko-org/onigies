"""Índice de sesiones con rutas tocadas. Complemento de credit.py: sirve para
ver de un vistazo qué tocó cada sesión, no para valuar (eso lo hace credit.py).

Uso:  python3 sess.py [minutos_de_hueco]   (por omisión 20)
El proyecto y las raíces salen de la misma configuración que credit.py.
"""
import collections
import datetime
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import credit as C

ROOT, ROOTS, BASE, AUDIT = C.resolve_config(sys.argv[1:])
GAP = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 20

files = [p for p in glob.glob(BASE + "/**/*.jsonl", recursive=True)
         if not any(f in p for f in AUDIT)]

rows = []
for p in files:
    ts = []
    paths = collections.Counter()
    nuser = nass = ntool = 0
    firstuser = None
    for line in open(p, errors="replace"):
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except Exception:
            continue
        t = C.parse_ts(d.get("timestamp")) if d.get("timestamp") else None
        if t:
            ts.append(t)
        typ = d.get("type")
        msg = d.get("message") or {}
        if typ == "user" and not d.get("isMeta"):
            bl = C.blocks_of(msg)
            txt = C.text_of(bl)
            if txt:
                nuser += 1
                if firstuser is None:
                    firstuser = txt[:160]
        if typ == "assistant":
            nass += 1
            for b in C.blocks_of(msg):
                if b.get("type") == "tool_use":
                    ntool += 1
                    inp = b.get("input") or {}
                    for k in ("file_path", "notebook_path"):
                        if isinstance(inp.get(k), str):
                            paths[inp[k]] += 1
                    cmd = inp.get("command")
                    if isinstance(cmd, str):
                        for m in re.findall(r'[\w./-]*/[\w./-]+', cmd)[:6]:
                            paths[m] += 1
    if not ts:
        continue
    ts.sort()
    active = sum(g for g in ((b - a).total_seconds() / 60 for a, b in zip(ts, ts[1:]))
                 if g <= GAP)
    rows.append(dict(path=p, sid=os.path.basename(p)[:-6],
                     sub="/" in p[len(BASE) + 1:],
                     start=ts[0], end=ts[-1],
                     span=(ts[-1] - ts[0]).total_seconds() / 60,
                     active=active, nuser=nuser, nass=nass, ntool=ntool,
                     paths=paths, first=firstuser))

rows.sort(key=lambda r: r["start"])
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sessions.json")
json.dump([dict(r, paths=dict(r["paths"].most_common(40)),
                start=r["start"].isoformat(), end=r["end"].isoformat())
           for r in rows], open(out, "w"))
print("proyecto:", ROOT)
print("sessions:", len(rows), "->", out)
print("total active (top-level, gap=%d):" % GAP,
      round(sum(r["active"] for r in rows if not r["sub"]) / 60, 1), "h")
print("total active (all):", round(sum(r["active"] for r in rows) / 60, 1), "h")
