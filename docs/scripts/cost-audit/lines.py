"""Atribución de las horas netas de ONIGIES a los conceptos de la cotización.

Lee credit.json (bitácoras, ya repartidas con los otros proyectos) y
cost-audit.json (fracciones facturables), y reparte cada sesión, cada día
ciego del historial y cada día de git entre los conceptos según lo que se
trabajó ahí. Los mapeos son lectura de prompts, títulos y archivos tocados:
cada uno lleva su confianza. Se filtra al final, sobre el resultado completo.
"""
import collections, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
PRE, AI = 850, 1300

# Concepto -> (cotizado, grupo). «Base del dashboard» no tiene renglón: el
# texto de la cotización promete acceso con token y un dashboard, sin precio.
QUOTE = {
    "bd": (8000, "pagado"), "pop": (16000, "pagado"),
    "cp": (27000, "pagado"), "flow": (25000, "pagado"),
    "bp": (12000, "pagado"), "base": (0, "pagado"),
    "editor": (0, "extra"), "word": (0, "extra"),
    "infra": (0, "extra"), "coord": (0, "extra"),
}

# Sesiones (8 primeros caracteres del uuid) -> reparto entre conceptos.
# Lo que no aparece aquí va a «base» (sesiones cortas sin tema claro).
SESS = {
    "988a331d": {"bp": .5, "base": .5}, "f85f48da": {"bp": .7, "base": .3},
    "0a0e1ee9": "bp", "1b2d7e8d": "pop", "322595eb": "base",
    "37024685": "coord", "38c7d003": "bp", "4015b0d5": "bp",
    "5ecb87aa": "coord", "8799bf56": "bp", "9af23f16": "base",
    "092f9f2c": "infra", "56a5f2b5": "bp", "d83bc103": "base",
    "edbd287e": "coord", "0b8592e4": "base", "0f25018f": "base",
    "8801c064": "base", "9d899e38": "base", "c8383855": "base",
    "d8933adb": "base", "5c72ff05": "base", "cf323ba6": "base",
    "f94b34b0": "infra", "a354126c": "bp", "cd158c15": "base",
    "d159141c": "bp", "e472b042": "base", "f3739548": "bp",
    "412bb8c1": "base", "dd1fece1": "flow", "b6cbf935": "flow",
    "bc2c2af3": "flow", "cce143da": "base",
    "efaf46ad": "coord", "76f17a41": "infra", "06b7c6f6": "coord",
    "7d6f4791": "infra", "0fbef1b2": "infra", "26165889": "base",
    "58bb1e0c": "coord", "79ebcbaf": {"infra": .5, "flow": .5},
    "897c5118": "coord", "c549806c": "coord", "d589beaf": "infra",
    "d9bc4e19": "base", "ee07a69c": "pop", "f132539c": "base",
    "7e972e43": {"pop": .6, "bp": .2, "flow": .2}, "c8df5b52": "coord",
    "eecac25f": "coord", "5a6fd914": "pop",
    "3fa62a75": {"coord": .5, "pop": .5}, "4328191a": "infra",
    "463b00d6": "pop", "51bbedde": "pop", "5c645b6b": "pop",
    "9aa921bf": {"infra": .5, "pop": .5}, "ab1883c9": "pop",
    "dfd4cced": "pop", "7f446bc4": "flow", "1ce5d2b4": "pop",
    "07597e12": "infra", "3a6f82e1": "base", "9fe62aac": "base",
    "5401b385": "base", "0d557873": "editor", "503b55da": "word",
    "8e146f37": "editor", "3705a870": "coord", "d5ef9c1e": "editor",
    "03f1e4b9": "editor", "b055612f": "word", "b6c8a4f0": "coord",
    "fe66c195": "coord", "2d561ef3": "cp", "e45316c3": "infra",
    "6635e96d": "coord", "a7383a8d": "cp", "cd144c44": "cp",
    "fb5dabb8": {"cp": .6, "infra": .4},
}
# Ajustes del record que no viven en credit.json: la parte de ONIGIES de la
# sesión 803fabce (abierta en ~/.claude) y las sesiones que corrieron durante
# reuniones grabadas.
ADJUST = [("base", +0.18), ("editor", -0.11), ("cp", -0.08), ("cp", -0.10)]

# Días ciegos: horas centrales de blind.py, repartidas por lo que dicen los
# prompts de ese día. Git: 2.23 h por día activo, por los archivos tocados.
BLIND = {  # (horas, tarifa, reparto)
    "git 12-03": (2.227, PRE, {"bd": 1}),
    "git 12-08": (2.227, PRE, {"bd": 1}),
    "git 01-02": (2.227, PRE, {"bd": .6, "base": .4}),
    "git 01-04": (2.227, PRE, {"base": 1}),
    "git 01-12": (2.227, PRE, {"bp": .5, "bd": .25, "base": .25}),
    "git 01-17": (2.227, PRE, {"bp": 1}),
    "git 01-22": (2.227, PRE, {"bp": 1}),
    "git 01-26": (2.227, PRE, {"bp": .5, "base": .5}),
    "git 02-13": (2.227, PRE, {"base": 1}),
    "hist 02-25/27": (4.05, PRE, {"base": 1}),
    "hist 03-03": (0.88, AI, {"base": 1}),
    "hist 03-09": (0.45, AI, {"base": 1}),
    "hist 03-14": (0.19, AI, {"base": 1}),
    "hist 03-16": (0.905, AI, {"base": .5, "infra": .5}),
    "hist 06-16": (2.89, AI, {"flow": .5, "bp": .2, "infra": .3}),
    "hist 06-19": (0.22, AI, {"base": 1}),
    "hist 06-20": (1.675, AI, {"flow": .6, "base": .4}),
    "hist 06-23": (3.045, AI, {"flow": .4, "bp": .6}),
    "hist 06-24": (1.655, AI, {"flow": .7, "bp": .3}),
    "hist 06-25": (6.845, AI, {"flow": .5, "bp": .5}),
    "hist 06-26": (1.955, AI, {"flow": .8, "base": .2}),
    "hist 07-03": (4.085, AI, {"coord": .15, "bp": .35, "flow": .2,
                               "pop": .1, "infra": .2}),
    "hist 07-04": (2.14, AI, {"cp": 1}),
    "Miró": (6.0, PRE, {"coord": 1}),
    "reuniones": (362 / 60, AI, {"coord": 1}),
}


def split(target):
    return {target: 1.0} if isinstance(target, str) else target


def main():
    cred = json.load(open(os.path.join(HERE, "credit.json")))
    cfg = json.load(open(os.path.join(HERE, "cost-audit.json")))
    frac = {k: v[0] for k, v in cfg.get("billable_fraction", {}).items()}
    h = collections.defaultdict(lambda: [0.0, 0.0])  # [h pre-IA, h con IA]
    for s in cred["sessions"]:
        sid = s["sid"][:8]
        net = s["allocated_h"] * frac.get(sid, 1.0)
        for k, f in split(SESS.get(sid, "base")).items():
            h[k][1] += net * f
    for k, delta in ADJUST:
        h[k][1] += delta
    for hours, rate, dist in BLIND.values():
        for k, f in dist.items():
            h[k][0 if rate == PRE else 1] += hours * f
    tot_h = tot_c = 0
    print(f"{'concepto':8} {'cotizado':>9} {'h pre':>6} {'h IA':>6} "
          f"{'h':>6} {'costo':>8} {'dif':>8}")
    for k, (q, g) in QUOTE.items():
        pre, ai = h[k]
        cost = pre * PRE + ai * AI
        tot_h += pre + ai
        tot_c += cost
        print(f"{k:8} {q:9,} {pre:6.1f} {ai:6.1f} {pre + ai:6.1f} "
              f"{cost:8,.0f} {cost - q:8,.0f}")
    print(f"{'total':8} {'':9} {'':6} {'':6} {tot_h:6.1f} {tot_c:8,.0f}")


if __name__ == "__main__":
    main()
