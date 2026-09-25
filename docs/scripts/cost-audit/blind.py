"""Periodos ciegos: días con prompts en history.jsonl pero sin bitácora.

Calibra horas por prompt y por ventana diaria sobre los días que tienen ambas
cosas, contando los prompts SIEMPRE desde history (el subconteo de prompts
encolados se cancela en los dos lados del cociente), y aplica el cociente a
los días ciegos.

Las horas de calibración son NETAS: cada sesión entra por su fracción
facturable de cost-audit.json (billable_fraction), porque un cociente
calculado con horas personales o de harness inflaría todo lo que se estima
con él.
"""
import collections, datetime, json, os, statistics

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
TZ = datetime.timezone(datetime.timedelta(hours=-6))
CUT = 6
PERIODS = [("2026-02-25", "2026-03-01"), ("2026-03-02", "2026-03-16"),
           ("2026-06-16", "2026-07-04"), ("2026-07-05", "2026-07-27")]
GIT_DAYS = 9


def day(t):
    return (t.astimezone(TZ) - datetime.timedelta(hours=CUT)).date()


cfg = json.load(open(os.path.join(HERE, "cost-audit.json")))
frac = {k: v[0] for k, v in cfg.get("billable_fraction", {}).items()}
exclude = cfg.get("blind_exclude_days", {})
day_from = {k: v[0] for k, v in cfg.get("blind_day_from", {}).items()}
min_prompts = cfg.get("blind_min_prompts", 1)

cred = json.load(open(os.path.join(HERE, "credit.json")))
gross = collections.defaultdict(float)
logged = collections.defaultdict(float)
for s in cred["sessions"]:
    d = day(datetime.datetime.fromisoformat(s["start"]))
    gross[d] += s["allocated_h"]
    logged[d] += s["allocated_h"] * frac.get(s["sid"][:8], 1.0)

hist = collections.defaultdict(list)
for line in open(os.path.expanduser("~/.claude/history.jsonl")):
    try:
        d = json.loads(line)
    except Exception:
        continue
    p = d.get("project") or ""
    if not (p == ROOT or p.startswith(ROOT + "/")):
        continue
    t = datetime.datetime.fromtimestamp(d["timestamp"] / 1000, datetime.timezone.utc)
    hist[day(t)].append(t)

cal = [(dd, len(ts), logged[dd], (max(ts) - min(ts)).total_seconds() / 3600)
       for dd, ts in hist.items() if gross.get(dd, 0) > 0]
tot_h = sum(c[2] for c in cal); tot_p = sum(c[1] for c in cal)
tot_w = sum(c[3] for c in cal)
per_prompt = tot_h / tot_p
per_window = tot_h / tot_w if tot_w else 0
per_day = tot_h / len(cal)
print("días de calibración: %d | prompts %d | horas netas %.2f (brutas %.2f)"
      % (len(cal), tot_p, tot_h, sum(gross[c[0]] for c in cal)))
print("h por prompt: %.3f | mediana diaria %.3f" % (
    per_prompt, statistics.median(c[2] / c[1] for c in cal)))
print("h por hora de ventana: %.3f" % per_window)
print("h por día activo: %.2f  -> git, %d días: %.2f h"
      % (per_day, GIT_DAYS, per_day * GIT_DAYS))

print("\n== días ciegos (history sin bitácora)")
rows = []
for dd in sorted(d for d in hist if gross.get(d, 0) == 0):
    ts = sorted(hist[dd]); raw = len(ts); note = ""
    key = dd.isoformat()
    if key in day_from:
        hh, mm = map(int, day_from[key].split(":"))
        lim = datetime.datetime.combine(dd, datetime.time(hh, mm), TZ)
        ts = [t for t in ts if t >= lim]
        note = "desde %s" % day_from[key]
    if key in exclude:
        ts, note = [], "excluido"
    elif len(ts) < min_prompts:
        ts, note = [], "un solo prompt"
    n = len(ts)
    w = (max(ts) - min(ts)).total_seconds() / 3600 if ts else 0.0
    hp, hw = n * per_prompt, w * per_window
    rows.append((dd, raw, n, w, hp, hw))
    print("  %s  prompts %3d usados %3d  ventana %5.2f h  -> %.2f | %.2f  %s"
          % (dd, raw, n, w, hp, hw, note))

print("\n== por periodo: días con prompts, prompts brutos, días usados, "
      "prompts usados, h por prompt, h por ventana, central")
for a, b in PERIODS:
    sel = [r for r in rows if a <= r[0].isoformat() <= b]
    used = [r for r in sel if r[2]]
    hp = sum(r[4] for r in sel); hw = sum(r[5] for r in sel)
    print("  %s → %s  %2d  %4d  %2d  %4d  %6.2f  %6.2f  %6.2f"
          % (a, b, len(sel), sum(r[1] for r in sel), len(used),
             sum(r[2] for r in sel), hp, hw, (hp + hw) / 2))
