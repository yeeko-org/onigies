"""Modelo de crédito de horas (rediseño del 28-ago-2026).

Cada evidencia (hueco humano, turno de máquina, marcador de presencia,
escritura, lectura) aporta un intervalo con una tasa de crédito, y en cada
instante gana la tasa máxima — nunca se suman. Sobre eso se monta una línea de
tiempo global entre TODOS los proyectos: cada instante se acredita una sola vez
y se reparte entre los proyectos activos en proporción a su densidad de
registros. Al final, ningún proyecto ni la suma pueden pasar del 95 % del reloj
de pared.

El script no está atado a ningún proyecto: infiere el repo desde su propia
ubicación (docs/scripts/cost-audit/ -> raíz del repo) y admite overrides por CLI
o por un cost-audit.json hermano.

Uso:
    python3 credit.py                      # reporte completo del proyecto inferido
    python3 credit.py --project-root PATH  # audita otro repo
    python3 credit.py --extra-root PATH    # segundo cwd que también es del cliente
    python3 credit.py --from 2026-08-26T19:45 --to 2026-08-28T13:15
    python3 credit.py --sessions           # + detalle sesión por sesión
    python3 credit.py --no-global          # sin reparto entre proyectos (modo viejo)
    python3 credit.py --include-meta       # incluye las sesiones de la propia auditoría
    python3 credit.py --filter REGEX       # bucket por título/rama
    python3 credit.py --paths REGEX [--share F]   # bucket por archivos tocados
    python3 credit.py --out FILE           # nombre del json de salida
"""

import collections
import datetime
import glob
import hashlib
import json
import os
import re
import sys

PROJECTS = os.path.expanduser("~/.claude/projects")
ARCHIVE = os.path.expanduser("~/.claude/session-logs-archive/projects")
HERE = os.path.dirname(os.path.abspath(__file__))

TZ = datetime.timezone(datetime.timedelta(hours=-6))  # CDMX, sin horario de verano
DAY_CUT = 6  # el día operativo empieza a las 06:00 locales (Ricardo trabaja
             # de madrugada y con las 05:00 se le partía la jornada en dos)

# Las tres magnitudes de tiempo del modelo son distintas y no se mezclan:
#
#   ESCRITURA        se mide por contenido (caracteres / CHARS_PER_MIN). No
#                    lleva tope: si el texto existe, el tiempo de teclearlo
#                    existió. Lo que tiene es un sitio donde caber, no un techo.
#   HUECO HUMANO     es una PRESUNCIÓN de presencia, no una medición: entre el
#                    fin del trabajo de máquina y el siguiente prompt se supone
#                    que Ricardo seguía ahí. Por ser presunción lleva tope
#                    —HUMAN_GAP_CAP— y por eso ese tope no se toca para
#                    compensar lo que falle en otra parte del modelo.
#   HUECO DE MÁQUINA mide si el turno seguía vivo: un silencio mayor que
#                    MACHINE_GAP_MAX significa que no había nada corriendo, y
#                    ese tramo se descarta en vez de acreditarse a fracción.
HUMAN_GAP_CAP = 20 * 60          # presunción de presencia: tope, no medición
MACHINE_GAP_MAX = 30 * 60        # silencio mayor a esto no es máquina trabajando
COMMAND_BEFORE = 3 * 60          # comando pegado: se arma antes de enviarlo
COMMAND_AFTER = 1 * 60           # y se mira el resultado un momento después
FRACTION = {"default": 0.35, "plan": 0.35, "auto": 0.15, "acceptEdits": 0.15}
FLOOR = {"default": 80.0, "plan": 80.0, "auto": 40.0, "acceptEdits": 40.0}
MODE_PIVOT = (2, 1, 216)         # antes -> default; desde aquí -> auto
MARKER_BEFORE = 3.5 * 60
MARKER_AFTER = 2.5 * 60
CHARS_PER_MIN = 90.0
WORDS_PER_MIN = 150.0
DENSITY_WIN = 15 * 60            # ventana de densidad para repartir el instante
WALL_CAP = 0.95                  # nadie acredita más del 95 % de su reloj
PASTE_MIN_LEN = 16               # línea mínima para buscarla como pegada
LIVE_GAP_MAX = 30 * 60           # hueco máximo para considerar viva una sesión
DEDUP_WINDOW = 5 * 60            # ventana para detectar un prompt reenviado
DEDUP_MIN_LEN = 200              # largo mínimo para comparar dos prompts por texto
# Qué le bloquea el paso a la escritura que se coloca hacia atrás:
#   "human" (por omisión) solo las sesiones ajenas donde Ricardo estaba al
#           teclado; un turno de máquina ajeno no bloquea, porque el modelo ya
#           le acredita su 15-35 % y el resto es el hueco en el que teclea aquí
#   "all"   cualquier sesión ajena con el reloj corriendo
WRITING_BLOCKS = "human"

RATE_AI = 1300.0

SYSREM = re.compile(r"<system-reminder>.*?</system-reminder>", re.S)
INTERRUPT = re.compile(r"\[Request interrupted by user[^\]]*\]")
TAG_START = re.compile(r"^<[a-zA-Z][\w-]*>")
HUMAN_TAGS = ("<command-name>",)
BASH_INPUT = re.compile(r"^\s*<bash-input>", re.I)

# Un rechazo de herramienta se reconoce por su cadena de apertura, anclada al
# principio del resultado. Sin anclar, la sola MENCIÓN de la frase basta —y el
# código de este script contiene ambas cadenas, así que leerlo se acreditaba
# como si Ricardo lo hubiera tecleado.
REJECTION_START = re.compile(
    r"^(?:Error:\s*)?The user doesn't want to proceed with this tool use\.", re.I)
REJECTION_MARK = "the user said:"

# Firmas de salida de consola, log o traza: nadie las teclea.
CONSOLE = re.compile(
    r"(^\s*(Traceback|File \"|\s+at [\w.$]+\s*\()"
    r"|^\s*\[?\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}"       # timestamp de log
    r"|^\s*\d{2}:\d{2}:\d{2}[.,]\d+"
    r"|\b(ERROR|WARN|WARNING|DEBUG|INFO|CRITICAL|FATAL)\b\s*[:\]]"
    r"|^\s*\[(nuxt|vite|webpack|nitro|vue|node|pm2|supervisor)\b"
    r"|^\s*(Error|TypeError|ValueError|KeyError|AttributeError|SyntaxError|"
    r"ReferenceError|RuntimeError|ImportError|OSError|IOError)\b\s*:"
    r"|^\s*at\s+\S+\s+\(.*:\d+:\d+\)"
    r"|^[\w./~-]+\.\w{1,5}:\d+(:\d+)?\b"              # ruta:linea[:col]
    r"|^\s*\+\+\+|^\s*---\s|^\s*@@ "                  # diff
    r"|https?://\S{15,}"                                   # URL larga
    r"|^\s*/[\w.@/~-]+\.\w{1,6}\b"                      # ruta absoluta con extensión
    r"|^\s*\S{12,}$(?=.*[./?])"                            # token solo, sin espacios
    r"|\?v=[0-9a-f]{6,}"                                   # cache-buster de bundler
    r"|^_?[A-Z][A-Z0-9_]{2,}\s*=\s"                      # volcado de settings
    r"|^\s*(Request (Method|URL)|Django Version|Exception (Type|Value|"
    r"Location)|Python (Executable|Version|Path)|Server time|Raised during)"
    r"\s*:"                                               # página de debug
    r"|^\s*[A-Za-z]:\\"                                  # ruta de Windows
    r")")


# ------------------------------------------------------------- configuración

def resolve_config(argv):
    """Devuelve (project_root, roots, base_dir, audit_sessions).

    Orden: CLI > cost-audit.json hermano > inferencia por la ruta del script.
    """
    cfg = {}
    p = os.path.join(HERE, "cost-audit.json")
    if os.path.exists(p):
        try:
            cfg = json.load(open(p))
        except Exception:
            cfg = {}
    # inferencia: docs/scripts/cost-audit/ -> raíz del repo tres niveles arriba
    guess = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
    root = arg_of(argv, "--project-root") or cfg.get("project_root") or guess
    root = os.path.abspath(os.path.expanduser(root))
    roots = [root]
    for extra in (arg_all(argv, "--extra-root") or cfg.get("extra_roots") or []):
        roots.append(os.path.abspath(os.path.expanduser(extra)))
    base = arg_of(argv, "--base") or cfg.get("base") or os.path.join(
        PROJECTS, encode_project_dir(root))
    audit = tuple(cfg.get("audit_sessions") or ())
    audit += tuple(arg_all(argv, "--audit-session") or ())
    return root, tuple(roots), base, audit


def encode_project_dir(path):
    """Claude Code guarda las bitácoras en ~/.claude/projects/<ruta codificada>,
    con «/», «.» y «_» convertidos en «-»."""
    return re.sub(r"[/._]", "-", path)


def arg_of(argv, flag):
    return argv[argv.index(flag) + 1] if flag in argv else None


def arg_all(argv, flag):
    out = []
    for i, a in enumerate(argv):
        if a == flag and i + 1 < len(argv):
            out.append(argv[i + 1])
    return out


def parse_ts(s):
    try:
        return datetime.datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except Exception:
        return None


def parse_local(s):
    """Fecha de CLI, interpretada en hora local."""
    d = parse_ts(s)
    if d is None:
        return None
    return d if d.tzinfo else d.replace(tzinfo=TZ)


def local(dt):
    return dt.astimezone(TZ)


def cut_date(dt):
    return (local(dt) - datetime.timedelta(hours=DAY_CUT)).date()


def version_tuple(v):
    try:
        return tuple(int(x) for x in (v or "0").split(".")[:3])
    except Exception:
        return (0, 0, 0)


# ------------------------------------------------------------ texto

def blocks_of(msg):
    c = (msg or {}).get("content")
    if isinstance(c, str):
        return [{"type": "text", "text": c}]
    if isinstance(c, list):
        return [b for b in c if isinstance(b, dict)]
    return []


def text_of(blocks):
    return "\n".join(b.get("text", "") for b in blocks if b.get("type") == "text")


def clean(text):
    """Texto humano neto: sin system-reminders ni marcas de interrupción."""
    return INTERRUPT.sub("", SYSREM.sub("", text or "")).strip()


def word_count(text):
    return len(clean(text).split())


def norm_line(line):
    """Normaliza una línea para compararla con lo ya visto: espacios colapsados."""
    return " ".join(line.split())


def line_key(line):
    n = norm_line(line)
    if len(n) < PASTE_MIN_LEN:
        return None
    return hashlib.blake2b(n.encode("utf-8", "replace"), digest_size=8).digest()


def iter_text_lines(d):
    """Todas las líneas de texto que un registro pone en circulación: sirven de
    corpus contra el que se detecta lo pegado."""
    out = []
    msg = d.get("message")
    for b in blocks_of(msg):
        t = b.get("type")
        if t == "text":
            out.append(b.get("text", ""))
        elif t == "tool_result":
            c = b.get("content")
            if isinstance(c, str):
                out.append(c)
            elif isinstance(c, list):
                for x in c:
                    if isinstance(x, dict) and isinstance(x.get("text"), str):
                        out.append(x["text"])
    tr = d.get("toolUseResult")
    if isinstance(tr, str):
        out.append(tr)
    elif isinstance(tr, dict):
        for k in ("stdout", "stderr", "content", "file", "output"):
            v = tr.get(k)
            if isinstance(v, str):
                out.append(v)
            elif isinstance(v, dict) and isinstance(v.get("content"), str):
                out.append(v["content"])
    for chunk in out:
        for line in chunk.splitlines():
            yield line


# -------------------------------------------------- tecleado vs. pegado

def structural_paste(lines):
    """Marca (por índice) las líneas que son pegado por su sola forma:
    bloques cercados, sangría de 2+ espacios, cita, o firma de consola."""
    marked = set()
    fenced = False
    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith("```"):
            marked.add(i)
            fenced = not fenced
            continue
        if fenced:
            marked.add(i)
            continue
        if line.startswith("  ") or s.startswith(">"):
            marked.add(i)
            continue
        if CONSOLE.search(line):
            marked.add(i)
    return marked


def typed_chars(text, echoed=frozenset()):
    """Caracteres realmente tecleados en un prompt.

    Se descuentan: (a) lo estructuralmente pegado (cercado, sangrado, citado,
    con firma de consola) y (b) las líneas que `echoed` marca por haber
    aparecido antes ese mismo día en cualquier proyecto. Las notas propias de
    Ricardo, aunque las pegue, cuentan como tecleadas: son escritura suya. El
    código escrito a mano y pegado se pierde a sabiendas.
    """
    lines = clean(text).splitlines()
    skip = structural_paste(lines)
    n = 0
    for i, line in enumerate(lines):
        if i in skip:
            continue
        k = line_key(line)
        if k is not None and k in echoed:
            continue
        n += len(line) + 1
    return max(0, n)


def prompt_candidates(recs):
    """Líneas de los prompts humanos que valdría la pena buscar en el corpus."""
    out = collections.defaultdict(dict)   # dia -> clave -> ts del prompt
    for d in recs:
        if not is_human_prompt(d):
            continue
        lines = clean(text_of(blocks_of(d.get("message")))).splitlines()
        skip = structural_paste(lines)
        day = cut_date(d["_ts"])
        for i, line in enumerate(lines):
            if i in skip:
                continue
            k = line_key(line)
            if k is None:
                continue
            prev = out[day].get(k)
            if prev is None or d["_ts"] < prev:
                out[day][k] = d["_ts"]
    return out


def scan_echoes(candidates, dirs, a=None, b=None):
    """Segunda pasada sobre TODOS los proyectos: marca las líneas candidatas que
    ya habían aparecido antes, el mismo día operativo, en cualquier bitácora."""
    echoed = set()
    if not candidates:
        return echoed
    for d in dirs:
        for p in glob.iglob(d + "/**/*.jsonl", recursive=True):
            for line in open(p, errors="replace"):
                line = line.strip()
                if not line:
                    continue
                try:
                    o = json.loads(line)
                except Exception:
                    continue
                ts = parse_ts(o.get("timestamp")) if o.get("timestamp") else None
                if ts is None:
                    continue
                if (a and ts < a - datetime.timedelta(days=1)) or (b and ts > b):
                    continue
                day = cut_date(ts)
                cand = candidates.get(day)
                if not cand:
                    continue
                for txt in iter_text_lines(o):
                    k = line_key(txt)
                    if k is None or k in echoed:
                        continue
                    first = cand.get(k)
                    if first is not None and ts < first:
                        echoed.add(k)
    return echoed


# ---------------------------------------------------------------- carga

def load_records(base, roots, a=None, b=None, stats=None):
    """(sesiones, meta). Cada sesión es la lista de registros ordenados por
    timestamp, con los subagentes fundidos en su sesión padre. La atribución es
    por el `cwd` de cada registro: las carpetas mienten."""
    stats = stats if stats is not None else collections.Counter()
    files = []
    # El árbol vivo lo poda la retención; el archivo guarda lo migrado de
    # Windows y lo ya borrado. Se leen los dos y el uuid deduplica.
    bases = [base]
    twin = os.path.join(ARCHIVE, os.path.basename(base))
    if os.path.isdir(twin) and os.path.abspath(twin) != os.path.abspath(base):
        bases.append(twin)
    for bd in bases:
        for p in sorted(glob.glob(bd + "/**/*.jsonl", recursive=True)):
            rel = p[len(bd) + 1:].split("/")
            if len(rel) == 1:
                files.append((rel[0][:-6], p, False))
            elif len(rel) == 3 and rel[1] == "subagents":
                files.append((rel[0], p, True))
            # workflows/ y demás quedan fuera

    seen = set()
    by_sid = collections.defaultdict(list)
    meta = collections.defaultdict(dict)

    for sid, path, is_sub in files:
        cwds = collections.Counter()
        raw = []
        for line in open(path, errors="replace"):
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                stats["unparsed_lines"] += 1
                continue
            raw.append(d)
            if d.get("cwd"):
                cwds[d["cwd"]] += 1
        dom = cwds.most_common(1)[0][0] if cwds else None
        meta[sid].setdefault("cwds", collections.Counter())
        meta[sid]["cwds"].update(cwds)

        for d in raw:
            t = d.get("type")
            if t == "custom-title":
                meta[sid]["custom"] = d.get("customTitle")
            elif t == "ai-title":
                meta[sid].setdefault("ai", d.get("aiTitle"))
            elif t == "agent-name":
                meta[sid].setdefault("agent", d.get("agentName"))
            if d.get("slug"):
                meta[sid].setdefault("slug", d["slug"])
            if d.get("gitBranch"):
                meta[sid].setdefault("branches", collections.Counter())
                meta[sid]["branches"][d["gitBranch"]] += 1

            ts = parse_ts(d.get("timestamp")) if d.get("timestamp") else None
            if ts is None:
                continue
            stats["records_with_ts"] += 1
            if (a and ts < a) or (b and ts > b):
                stats["out_of_window"] += 1
                continue
            u = d.get("uuid")
            if u:
                if u in seen:
                    stats["dup_uuid"] += 1
                    continue
                seen.add(u)
            cwd = d.get("cwd") or dom
            if roots and cwd and not any(cwd == r or cwd.startswith(r + "/")
                                         for r in roots):
                stats["excluded_foreign_cwd"] += 1
                continue
            d["_ts"] = ts
            d["_sub"] = is_sub
            by_sid[sid].append(d)
            stats["records_kept"] += 1

    for sid in by_sid:
        by_sid[sid].sort(key=lambda d: d["_ts"])
    return by_sid, meta


def title_of(sid, meta):
    m = meta.get(sid, {})
    return (m.get("custom") or m.get("ai") or m.get("agent")
            or m.get("slug") or sid[:8])


# ---------------------------------------- clasificación de registros

def is_human_prompt(d):
    if d.get("type") != "user":
        return False
    # Los briefings a subagentes los escribe el asistente, no Ricardo.
    if d.get("_sub") or d.get("isSidechain"):
        return False
    o = d.get("origin")
    if isinstance(o, dict) and o.get("kind"):
        return o["kind"] == "human"
    if d.get("isMeta"):
        return False
    bl = blocks_of(d.get("message"))
    if any(b.get("type") in ("tool_result", "tool_use") for b in bl):
        return False
    txt = SYSREM.sub("", text_of(bl)).strip()
    if not txt:
        return False
    if INTERRUPT.sub("", txt).strip() == "":
        return False  # marcador de presencia, no prompt
    if txt.startswith(HUMAN_TAGS):
        return True
    if TAG_START.match(txt):
        return False
    return True


def pasted_commands(recs, idx_human):
    """Índices de prompts que son un comando, no prosa.

    Dos formas: el modo bash del prompt (`<bash-input>`) y el comando que el
    asistente acaba de proponer y Ricardo devuelve tal cual. Ninguno se teclea
    a razón de 90 c/min —se pega, o se copia de la línea de arriba—, así que
    acreditarlos por longitud regalaba minutos: un comando de 400 caracteres
    valía cuatro minutos y medio de redacción. Cuentan como interacción, con un
    crédito fijo de 4 minutos (Ricardo: «3 o 4 minutos máximo»)."""
    offered = set()
    for d in recs:
        if d.get("type") != "assistant":
            continue
        for b in blocks_of(d.get("message")):
            if b.get("type") == "tool_use" and b.get("name") == "Bash":
                cmd = (b.get("input") or {}).get("command")
                if isinstance(cmd, str) and cmd.strip():
                    offered.add(" ".join(cmd.split()))
    out = set()
    for i in idx_human:
        txt = clean(text_of(blocks_of(recs[i].get("message"))))
        if BASH_INPUT.match(txt) or " ".join(txt.split()) in offered:
            out.add(i)
    return out


def duplicate_prompts(recs, idx_human):
    """Índices de prompts reenviados, que no son trabajo nuevo.

    Dos criterios en OR, no en cascada. El `promptId` atrapa el reenvío que el
    harness reconoce como el mismo; el texto atrapa el que no: cuando Ricardo
    vuelve a mandar lo mismo a mano —el caso de c753d5d5, 3,316 caracteres
    repetidos a los 21 segundos— el harness emite **dos promptId distintos**, y
    solo comparando el contenido se ve que es un envío repetido y no media hora
    más de tecleo."""
    dup = set()
    seen_id = set()
    recent = []          # (ts, texto) dentro de la ventana
    for i in idx_human:
        d = recs[i]
        pid = d.get("promptId")
        txt = clean(text_of(blocks_of(d.get("message"))))
        ts = d["_ts"]
        recent = [(t, x) for t, x in recent
                  if (ts - t).total_seconds() <= DEDUP_WINDOW]
        if (pid is not None and pid in seen_id) or (
                len(txt) >= DEDUP_MIN_LEN and any(x == txt for _, x in recent)):
            dup.add(i)
            continue
        if pid is not None:
            seen_id.add(pid)
        recent.append((ts, txt))
    return dup


def is_real_prompt(d):
    """Prompt humano con contenido propio: ni invocación de comando ni monosílabo.
    Una sesión sin ninguno no es trabajo — es una sesión abierta por error."""
    if not is_human_prompt(d):
        return False
    txt = clean(text_of(blocks_of(d.get("message"))))
    if txt.startswith(HUMAN_TAGS):
        return False
    return len(txt) > 3


def is_machine_work(d):
    """Registro que prueba que la máquina estaba trabajando en ese instante."""
    if d.get("type") == "assistant":
        return True
    if d.get("type") == "user":
        return any(b.get("type") == "tool_result"
                   for b in blocks_of(d.get("message")))
    return False


def prompt_mode(d):
    """(fracción, piso, etiqueta) del prompt que gobierna el turno."""
    pm = d.get("permissionMode")
    if pm in FRACTION:
        return FRACTION[pm], FLOOR[pm], pm
    guess = "auto" if version_tuple(d.get("version")) >= MODE_PIVOT else "default"
    return FRACTION[guess], FLOOR[guess], "missing->" + guess


def markers_of(d):
    """Timestamps donde hay evidencia directa de que Ricardo estaba al teclado."""
    out = []
    ts = d["_ts"]
    bl = blocks_of(d.get("message")) if d.get("type") == "user" else []
    if any(INTERRUPT.search(b.get("text", "")) for b in bl
           if b.get("type") == "text"):
        out.append(("esc", ts))
    tr = d.get("toolUseResult")
    if isinstance(tr, dict):
        if tr.get("userModified") is True:
            out.append(("userModified", ts))
        # La respuesta a una AskUserQuestion se reconoce por su forma: el
        # resultado trae `questions` y `answers`. Buscar el nombre de la
        # herramienta dentro del texto del resultado es la misma trampa que el
        # rechazo autorreferencial: cualquier bitácora o documento que la
        # mencione se acreditaba como si Ricardo hubiera contestado.
        if "questions" in tr and "answers" in tr:
            out.append(("ask", ts))
    # Mismo ancla que rejection_text: mencionar la frase no es rechazarla.
    if is_rejection(d):
        out.append(("rejection", ts))
    a = d.get("attachment")
    if isinstance(a, dict) and a.get("type") in ("opened_file_in_ide",
                                                 "selected_lines_in_ide"):
        out.append(("ide", ts))
    return out


def result_string(d):
    """El resultado de herramienta como texto plano, si lo hay."""
    tr = d.get("toolUseResult")
    s = tr if isinstance(tr, str) else ""
    for b in blocks_of(d.get("message")) if d.get("type") == "user" else []:
        if b.get("type") == "tool_result":
            c = b.get("content")
            if isinstance(c, str):
                s = c
    return s


def is_rejection(d):
    """Verdadero solo si el resultado ES un rechazo, no si lo menciona."""
    return bool(REJECTION_START.match(result_string(d).strip()))


def rejection_text(d):
    """Motivo tecleado al rechazar una herramienta: cuenta como escritura.

    Solo si el resultado abre con la cadena de rechazo. Un listado de código o
    una bitácora que contenga la frase no es un rechazo: sin este ancla, leer
    el propio credit.py acreditaba 17,535 caracteres —194 minutos— de
    escritura fantasma, dos veces."""
    if not is_rejection(d):
        return ""
    s = result_string(d)
    i = s.lower().find(REJECTION_MARK)
    return s[i + len(REJECTION_MARK):].strip() if i >= 0 else ""


# ------------------------------------- reloj vivo de las demás sesiones

def collect_live(dirs, a=None, b=None):
    """Intervalos en que CADA sesión tuvo el reloj corriendo, leídos solo de los
    timestamps de sus registros: dos consecutivos separados por menos de
    LIVE_GAP_MAX cuentan como sesión viva entre ellos. Deliberadamente no usa el
    crédito: si lo usara habría circularidad con la escritura que este mapa
    sirve para colocar."""
    ts_by = collections.defaultdict(list)
    for d in dirs:
        for p in glob.iglob(d + "/**/*.jsonl", recursive=True):
            rel = p[len(d) + 1:].split("/")
            sid = rel[0][:-6] if len(rel) == 1 else rel[0]
            for line in open(p, errors="replace"):
                i = line.find('"timestamp":"')
                if i < 0:
                    continue
                j = line.find('"', i + 13)
                t = parse_ts(line[i + 13:j]) if j > 0 else None
                if t is None or (a and t < a) or (b and t > b):
                    continue
                # Marca barata de «aquí estaba Ricardo, no la máquina sola».
                hum = ('"kind":"human"' in line or '"promptSource":"typed"' in line
                       or '"promptSource":"queued"' in line)
                ts_by[sid].append((t, hum))
    out = []
    for sid, ts in ts_by.items():
        ts.sort()
        for (x, hx), (y, hy) in zip(ts, ts[1:]):
            if 0 < (y - x).total_seconds() <= LIVE_GAP_MAX:
                out.append((x, y, sid, hx or hy))
    out.sort()
    return out


def segment_owners(live):
    """Corta los intervalos vivos en segmentos disjuntos y anota cuántas
    sesiones cubren cada uno y, si es una sola, cuál. Con esto se responde en
    una sola pasada «¿estaba viva alguna sesión distinta de ésta?»."""
    if not live:
        return []
    pts = sorted({t for iv in live for t in iv[:2]})
    ev = collections.defaultdict(list)
    for x, y, sid, hum in live:
        ev[x].append((1, sid, hum))
        ev[y].append((-1, sid, hum))
    cur = collections.Counter()
    hum_cur = collections.Counter()
    segs = []
    for i, p in enumerate(pts[:-1]):
        for delta, sid, hum in ev.get(p, []):
            cur[sid] += delta
            if hum:
                hum_cur[sid] += delta
                if hum_cur[sid] <= 0:
                    del hum_cur[sid]
            if cur[sid] <= 0:
                del cur[sid]
        if cur:
            segs.append((p, pts[i + 1], len(cur),
                         next(iter(cur)) if len(cur) == 1 else None,
                         frozenset(hum_cur)))
    return segs


def merge_into(busy, ivs):
    """Añade intervalos a la lista ocupada y la deja disjunta y ordenada.
    La escritura ya colocada ocupa: el siguiente prompt no puede reutilizarla."""
    all_ = sorted([(x, y) for x, y in busy] + [(x, y) for x, y, _ in ivs])
    out = []
    for x, y in all_:
        if out and x <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], y))
        else:
            out.append((x, y))
    return out


def busy_for(segs, sid, only_human=False):
    """Segmentos ocupados por alguna sesión que NO es `sid`, ya fusionados.

    Con `only_human` solo bloquean los tramos donde la otra sesión tenía a
    Ricardo al teclado (algún extremo es prompt suyo). Un turno de máquina de
    otra sesión no bloquea: el modelo ya le acredita 15-35 % de atención, y el
    65-85 % restante es precisamente el hueco en el que Ricardo teclea en otra
    ventana. Es el sentido literal de «lo armé en los huecos»."""
    out = []
    for x, y, n, owner, hums in segs:
        if only_human:
            blocked = bool(hums - {sid})
        else:
            blocked = n >= 2 or owner != sid
        if blocked:
            if out and x <= out[-1][1]:
                out[-1] = (out[-1][0], max(out[-1][1], y))
            else:
                out.append((x, y))
    return out


def day_floor(anchor):
    """Las 06:00 locales del día operativo del ancla: hacia atrás, la escritura
    no cruza el corte de día."""
    return datetime.datetime.combine(cut_date(anchor),
                                     datetime.time(DAY_CUT), tzinfo=TZ)


def place_writing(anchor, secs, busy, floor=None):
    """Coloca `secs` de escritura hacia atrás desde `anchor` **ocupando el
    tiempo que estaba libre**: salta los instantes en que otra sesión tenía el
    reloj corriendo y sigue estirándose hacia atrás hasta completar sus minutos,
    sin cruzar el corte de día.

    El caso que fijó la regla: el briefing de 8,834 caracteres del 27-ago 13:15
    (sesión f465960e). Ricardo confirmó que lo armó «en distintos momentos,
    desde antes y en los huecos» y que le tomó ese tiempo. Un bloque contiguo
    pegado al prompt lo colocaba encima de dos sesiones que sí estaban vivas;
    repartirlo por los huecos libres es lo que de verdad pasó.

    `floor` es el tope hacia atrás. Solo el **primer prompt real** de la sesión
    puede retroceder hasta el corte de día, porque ése sí lo teclea Ricardo
    antes de que la sesión exista. De ahí en adelante el tope es el primer
    registro de la sesión: a media sesión casi nunca pega texto escrito antes
    de abrirla, y dejar que retrocediera más sería regalarle tiempo.

    Devuelve (intervalos, segundos que no cupieron antes del tope)."""
    import bisect
    if floor is None:
        floor = day_floor(anchor)
    out = []
    t = anchor
    left = secs
    idx = [x for x, _ in busy]
    while left > 0 and t > floor:
        i = bisect.bisect_right(idx, t) - 1
        if i >= 0 and busy[i][0] < t <= busy[i][1]:
            t = busy[i][0]          # dentro de tiempo ajeno: saltarlo entero
            continue
        # `t` ya está libre; el tope hacia atrás es el fin del ocupado anterior,
        # que no es `i` cuando `t` cayó justo en el inicio de `busy[i]`.
        j = i
        while j >= 0 and busy[j][1] > t:
            j -= 1
        lo = max(busy[j][1] if j >= 0 else floor, floor)
        avail = (t - lo).total_seconds()
        if avail <= 0:
            break
        take = min(avail, left)
        out.append((t - datetime.timedelta(seconds=take), t, 1.0))
        left -= take
        t = lo
    return out, left


# ------------------------------------------------ fusión de intervalos

def fuse(intervals):
    """Suma, en segundos, del máximo de tasas en cada instante cubierto.
    Devuelve (total_segundos_acreditados, tramos) con tramos = [(a,b,tasa)]."""
    if not intervals:
        return 0.0, []
    pts = sorted({t for iv in intervals for t in (iv[0], iv[1])})
    events = collections.defaultdict(list)
    for a, b, r in intervals:
        if b <= a:
            continue
        events[a].append(("+", r))
        events[b].append(("-", r))
    active = collections.Counter()
    total = 0.0
    tramos = []
    for i, p in enumerate(pts):
        for kind, r in events.get(p, []):
            if kind == "+":
                active[r] += 1
            else:
                active[r] -= 1
                if active[r] <= 0:
                    del active[r]
        if i + 1 < len(pts):
            dur = (pts[i + 1] - p).total_seconds()
            if active and dur > 0:
                r = max(active)
                total += dur * r
                tramos.append((p, pts[i + 1], r))
    return total, tramos


def union_hours(spans, a=None, b=None):
    """Reloj de pared cubierto por una lista de [(inicio, fin)], en horas."""
    ivs = []
    for x, y in spans:
        if a:
            x = max(x, a)
        if b:
            y = min(y, b)
        if y > x:
            ivs.append((x, y))
    ivs.sort()
    tot = 0.0
    ca = cb = None
    for x, y in ivs:
        if ca is None:
            ca, cb = x, y
        elif x <= cb:
            cb = max(cb, y)
        else:
            tot += (cb - ca).total_seconds()
            ca, cb = x, y
    if ca:
        tot += (cb - ca).total_seconds()
    return tot / 3600.0


# ------------------------------------------------------ modelo por sesión

def credit_session(sid, recs, meta, echoed=frozenset(), segs=None):
    if not recs:
        return None
    # Sesión sin ningún prompt humano de contenido: abierta por error o tecleada
    # de más. No acredita nada, ni siquiera cojines de presencia.
    if not any(is_real_prompt(d) for d in recs):
        return None

    intervals = []     # (inicio, fin, tasa)
    parts = collections.Counter()
    mode_split = collections.Counter()

    # anclas de encolado: contenido -> ts en que se pulsó enter
    enqueues = {}
    for d in recs:
        if d.get("type") == "queue-operation" and d.get("operation") == "enqueue":
            c = (d.get("content") or "").strip()
            if c:
                enqueues.setdefault(c[:200], d["_ts"])

    idx_human = [i for i, d in enumerate(recs) if is_human_prompt(d)]
    idx_human = [i for i in idx_human if i not in duplicate_prompts(recs, idx_human)]

    # --- escritura (prompts) y marcadores
    # La escritura puede caer antes del primer registro de la sesión: Ricardo
    # suele teclear el prompt antes de que la sesión exista. Ese intervalo entra
    # a la línea de tiempo global y compite en el reparto como cualquier otro.
    busy = busy_for(segs, sid, WRITING_BLOCKS == "human") if segs else []
    cmds = pasted_commands(recs, idx_human)
    # El primer prompt REAL de la sesión —no la invocación de /model o /clear
    # que suele abrirla— es el único que pudo teclearse antes de que la sesión
    # existiera, y el único que puede retroceder hasta el corte de día.
    first_real = next((d["_ts"] for d in recs if is_real_prompt(d)), None)
    session_start = recs[0]["_ts"]
    writing = 0.0
    writing_spill = 0.0
    pasted_chars = 0
    for i in idx_human:
        d = recs[i]
        txt = text_of(blocks_of(d.get("message")))
        if i in cmds:
            # Interacción, no redacción: crédito fijo del tamaño de un marcador.
            intervals.append((d["_ts"] - datetime.timedelta(seconds=COMMAND_BEFORE),
                              d["_ts"] + datetime.timedelta(seconds=COMMAND_AFTER),
                              1.0))
            parts["marker_command"] += 1
            pasted_chars += len(clean(txt))
            continue
        n = typed_chars(txt, echoed)
        pasted_chars += max(0, len(clean(txt)) - n)
        if n <= 0:
            continue
        anchor = enqueues.get(clean(txt)[:200], d["_ts"])
        secs = n / CHARS_PER_MIN * 60.0
        fl = day_floor(anchor) if d["_ts"] == first_real \
            else max(day_floor(anchor), session_start)
        ivs, left = place_writing(anchor, secs, busy, fl)
        intervals.extend(ivs)
        busy = merge_into(busy, ivs)
        writing += secs - left
        writing_spill += left

    for d in recs:
        for kind, ts in markers_of(d):
            intervals.append((ts - datetime.timedelta(seconds=MARKER_BEFORE),
                              ts + datetime.timedelta(seconds=MARKER_AFTER), 1.0))
            parts["marker_" + kind] += 1
        rt = rejection_text(d)
        if rt:
            secs = typed_chars(rt, echoed) / CHARS_PER_MIN * 60.0
            if secs > 0:
                ivs, left = place_writing(
                    d["_ts"], secs, busy,
                    max(day_floor(d["_ts"]), session_start))
                intervals.extend(ivs)
                busy = merge_into(busy, ivs)
                writing += secs - left
                writing_spill += left

    # --- turnos de máquina, lectura y huecos humanos
    machine = 0.0
    machine_floor = 0.0
    reading = 0.0
    bounds = idx_human + [len(recs)]
    for k in range(len(idx_human)):
        i = idx_human[k]
        nxt = bounds[k + 1]
        d = recs[i]
        frac, floor, label = prompt_mode(d)
        block = recs[i:nxt]
        # El turno de máquina termina en el último registro de trabajo real:
        # los attachments y snapshots que aparecen al regresar Ricardo horas
        # después no son máquina trabajando.
        work = [d] + [r for r in block if is_machine_work(r)]
        last = work[-1]
        # Nombre propio: `segs` es el mapa de reloj vivo que recibe la función.
        turn = [(a["_ts"], b["_ts"]) for a, b in zip(work, work[1:])
                if 0 < (b["_ts"] - a["_ts"]).total_seconds() <= MACHINE_GAP_MAX]
        dur = sum((b - a).total_seconds() for a, b in turn)
        if dur > 0:
            cred = min(dur, max(floor, frac * dur))
            r_eff = cred / dur
            for a, b in turn:
                intervals.append((a, b, r_eff))
            machine += cred
            machine_floor += min(dur, floor)
            mode_split[label] += dur
        # Frontera de lo que Ricardo pudo leer: el siguiente prompt suyo.
        limit = recs[nxt]["_ts"] if nxt < len(recs) else recs[-1]["_ts"]
        # lectura: último texto de asistente del turno (no de subagentes),
        # topada por el hueco real hasta el siguiente prompt humano
        for r in reversed(block):
            if r.get("type") == "assistant" and not r.get("_sub") \
                    and not r.get("isSidechain"):
                w = word_count(text_of(blocks_of(r.get("message"))))
                if w:
                    secs = w / WORDS_PER_MIN * 60.0
                    room = (limit - r["_ts"]).total_seconds()
                    secs = min(secs, max(0.0, room))
                    if secs > 0:
                        intervals.append(
                            (r["_ts"],
                             r["_ts"] + datetime.timedelta(seconds=secs), 1.0))
                        reading += secs
                break
        # hueco humano hasta el siguiente prompt
        if nxt < len(recs):
            gap = (recs[nxt]["_ts"] - last["_ts"]).total_seconds()
            if gap > 0:
                use = min(gap, HUMAN_GAP_CAP)
                intervals.append((last["_ts"],
                                  last["_ts"] + datetime.timedelta(seconds=use),
                                  1.0))

    credited, tramos = fuse(intervals)

    # --- piso por sesión, topado por el reloj REAL de la sesión
    ts_all = [d["_ts"] for d in recs]
    span = (ts_all[-1] - ts_all[0]).total_seconds()
    floor_sum = writing + reading + machine_floor
    floored = False
    if credited < min(floor_sum, span):
        credited = min(floor_sum, span)
        floored = True

    # --- método viejo, para comparar: huecos topados a 20 min
    old = sum(min((b - a).total_seconds(), HUMAN_GAP_CAP)
              for a, b in zip(ts_all, ts_all[1:])
              if (b - a).total_seconds() <= HUMAN_GAP_CAP)

    paths = collections.Counter()
    for d in recs:
        if d.get("type") != "assistant":
            continue
        for b in blocks_of(d.get("message")):
            if b.get("type") == "tool_use":
                inp = b.get("input") or {}
                for k in ("file_path", "notebook_path"):
                    if isinstance(inp.get(k), str):
                        paths[inp[k]] += 1

    m = meta.get(sid, {})
    cw = m.get("cwds", collections.Counter())
    br = m.get("branches", collections.Counter())
    return dict(
        sid=sid, title=title_of(sid, meta),
        credited_h=credited / 3600.0, old_h=old / 3600.0,
        span_h=span / 3600.0,
        start=ts_all[0], end=ts_all[-1],
        month=cut_date(ts_all[0]).strftime("%Y-%m"),
        cwd=cw.most_common(1)[0][0] if cw else "-",
        branch=br.most_common(1)[0][0] if br else "-",
        branches=dict(br.most_common(5)),
        writing_h=writing / 3600.0, writing_spill_h=writing_spill / 3600.0,
        reading_h=reading / 3600.0,
        machine_h=machine / 3600.0, n_prompts=len(idx_human),
        n_real_prompts=sum(1 for d in recs if is_real_prompt(d)),
        pasted_chars=pasted_chars,
        n_records=len(recs), floored=floored,
        markers=dict(parts), mode_split=dict(mode_split),
        paths=paths, n_paths=sum(paths.values()),
        tramos=tramos)


def month_breakdown(tramos):
    """Reparte horas acreditadas por mes usando el corte de día (DAY_CUT)."""
    per = collections.Counter()
    for a, b, r in tramos:
        per[cut_date(a).strftime("%Y-%m")] += (b - a).total_seconds() * r / 3600.0
    return per


# ------------------------------------------- línea de tiempo entre proyectos

def project_dirs():
    out = []
    for d in sorted(glob.glob(PROJECTS + "/*")):
        if os.path.isdir(d):
            out.append(d)
    if os.path.isdir(ARCHIVE):
        for d in sorted(glob.glob(ARCHIVE + "/*")):
            if os.path.isdir(d):
                out.append(d)
    return out


def foreign_buckets(base, roots, a=None, b=None, segs=None):
    """Tramos y timestamps de los DEMÁS proyectos, uno a uno, sin guardar sus
    registros: solo lo que hace falta para repartir el instante compartido."""
    out = {}
    ours = os.path.basename(base)
    for d in project_dirs():
        name = os.path.basename(d)
        if name == ours:
            continue
        # load_records ya lee el gemelo del archivo junto al árbol vivo
        if d.startswith(ARCHIVE) and os.path.isdir(os.path.join(PROJECTS, name)):
            continue
        by, meta = load_records(d, None, a, b)
        tr, ts, spans = [], [], []
        for sid, recs in by.items():
            # Los registros que en realidad son del proyecto auditado ya se
            # contaron por cwd allá; aquí no vuelven a entrar.
            dom = collections.Counter(r.get("cwd") for r in recs
                                      if r.get("cwd")).most_common(1)
            cwd = dom[0][0] if dom else None
            if cwd and roots and any(cwd == r or cwd.startswith(r + "/")
                                     for r in roots):
                continue
            s = credit_session(sid, recs, meta, segs=segs)
            if not s:
                continue
            tr += s["tramos"]
            ts += [r["_ts"] for r in recs]
            spans.append((recs[0]["_ts"], recs[-1]["_ts"]))
        if not tr:
            continue
        _, fused = fuse(tr)
        out.setdefault(name, dict(tramos=[], ts=[], spans=[]))
        out[name]["tramos"] += fused
        out[name]["ts"] += sorted(ts)
        out[name]["spans"] += spans
    for k in out:
        out[k]["ts"].sort()
        out[k]["tramos"].sort()
    return out


def allocate(buckets, a=None, b=None, attribute=None):
    """Reparto global: cada instante vale la tasa máxima entre los proyectos
    activos y se divide en proporción a la densidad de registros (+-15 min).

    Con `attribute=(nombre, sesiones)` baja el resultado al nivel de sesión en
    la misma pasada: cada instante en que el proyecto está activo se le imputa
    a la sesión que tenía ahí la tasa más alta (las simultáneas del mismo
    proyecto ya se colapsaron al fundir). Se acumulan dos cosas por sesión —lo
    fundido, con la tasa propia del proyecto, y lo asignado, con la tasa máxima
    global por su parte del reparto—, de modo que ambas suman exactamente los
    totales del proyecto sin necesidad de escalar por un factor.

    Devuelve (horas por proyecto, horas fusionadas totales, horas por sesión).
    """
    import bisect
    keys = list(buckets)
    idx = {}
    for k in keys:
        tr = sorted(buckets[k]["tramos"])
        idx[k] = ([x[0] for x in tr], tr, buckets[k]["ts"])

    ours, sess = attribute if attribute else (None, [])
    # Se ordena por el primer tramo, no por `start`: la escritura de un prompt
    # tecleado antes de abrir la sesión cae por delante de su primer registro.
    sidx = {}
    for x in sess:
        tr = sorted(x["tramos"])
        sidx[x["sid"]] = ([t[0] for t in tr], tr,
                          tr[0][0] if tr else None, tr[-1][1] if tr else None,
                          x["start"], x["end"])
    sess = sorted([x for x in sess if sidx[x["sid"]][1]],
                  key=lambda x: sidx[x["sid"]][2])
    sess_from = [sidx[x["sid"]][2] for x in sess]

    def owners(t):
        """Sesiones que se reparten el instante `t`, ya empatadas a la tasa
        máxima. Dos criterios, en este orden: gana la tasa más alta, y entre
        las empatadas —lo normal, porque la escritura y los huecos valen 1.0—
        gana la que tenía el reloj corriendo, no la que solo estira hacia ahí
        el crédito de escritura de un prompt que se tecleó después. Si aun así
        empatan, el instante se parte entre ellas."""
        best, bestr = [], 0.0
        for x in sess[:bisect.bisect_right(sess_from, t)]:
            st, tr, _, last, _, _ = sidx[x["sid"]]
            if last <= t:
                continue
            i = bisect.bisect_right(st, t) - 1
            if i < 0 or tr[i][1] <= t:
                continue
            r = tr[i][2]
            if r > bestr:
                best, bestr = [x["sid"]], r
            elif r == bestr:
                best.append(x["sid"])
        if len(best) > 1:
            live = [k for k in best if sidx[k][4] <= t < sidx[k][5]]
            if live:
                best = live
        return best

    def rate(k, t):
        st, tr, _ = idx[k]
        i = bisect.bisect_right(st, t) - 1
        return tr[i][2] if i >= 0 and tr[i][1] > t else 0.0

    def dens(k, x, y):
        _, _, ts = idx[k]
        lo = bisect.bisect_left(ts, x - datetime.timedelta(seconds=DENSITY_WIN))
        hi = bisect.bisect_right(ts, y + datetime.timedelta(seconds=DENSITY_WIN))
        return float(hi - lo)

    pts = sorted({t for k in keys for iv in idx[k][1] for t in iv[:2]})
    if a:
        pts = [a] + [p for p in pts if p > a]
    if b:
        pts = [p for p in pts if p < b] + [b]
    out = collections.Counter()
    per_fused = collections.Counter()
    per_alloc = collections.Counter()
    total = 0.0
    for x, y in zip(pts, pts[1:]):
        dur = (y - x).total_seconds()
        if dur <= 0:
            continue
        r = {k: rate(k, x) for k in keys}
        top = max(r.values()) if r else 0.0
        if top <= 0:
            continue
        total += dur * top
        act = [k for k, v in r.items() if v > 0]
        if len(act) == 1:
            share = 1.0
            out[act[0]] += dur * top
        else:
            w = {k: dens(k, x, y) for k in act}
            s = sum(w.values())
            if s <= 0:
                w = {k: 1.0 for k in act}
                s = float(len(act))
            for k in act:
                out[k] += dur * top * w[k] / s
            share = w[ours] / s if ours in w else 0.0
        if ours and r.get(ours, 0.0) > 0:
            sids = owners(x)
            if sids:
                n = float(len(sids))
                for sid in sids:
                    per_fused[sid] += dur * r[ours] / n
                    per_alloc[sid] += dur * top * share / n
    per = {sid: dict(fused_h=per_fused[sid] / 3600.0,
                     allocated_h=per_alloc[sid] / 3600.0)
           for sid in set(per_fused) | set(per_alloc)}
    return {k: v / 3600.0 for k, v in out.items()}, total / 3600.0, per


def attribute_sessions(sessions, per, cap_factor=1.0):
    """Vuelca sobre cada sesión lo que `allocate` ya calculó instante a
    instante. `cap_factor` es 1.0 salvo que el tope del 95 % haya recortado al
    proyecto, en cuyo caso el recorte se reparte igual entre sus sesiones."""
    for s in sessions:
        d = per.get(s["sid"], {})
        s["fused_h"] = d.get("fused_h", 0.0)
        s["allocated_h"] = d.get("allocated_h", 0.0) * cap_factor
    return sessions


def apply_caps(alloc, buckets, a=None, b=None):
    """Nadie acredita más del 95 % de su reloj de pared; la suma tampoco pasa
    del 95 % del reloj donde hubo actividad de cualquiera. Devuelve
    (alloc topada, avisos)."""
    notes = []
    out = dict(alloc)
    for k, v in list(out.items()):
        wall = union_hours(buckets[k]["spans"], a, b)
        cap = wall * WALL_CAP
        if v > cap:
            notes.append("tope por proyecto: %s %.2f -> %.2f h (reloj %.2f h)"
                         % (k, v, cap, wall))
            out[k] = cap
    allspans = [s for k in buckets for s in buckets[k]["spans"]]
    wall = union_hours(allspans, a, b)
    gcap = wall * WALL_CAP
    tot = sum(out.values())
    if tot > gcap and tot > 0:
        notes.append("tope global: %.2f -> %.2f h (reloj con actividad %.2f h)"
                     % (tot, gcap, wall))
        f = gcap / tot
        out = {k: v * f for k, v in out.items()}
    return out, notes


# --------------------------------------------------------- offline

def offline_minutes(docs):
    out = []
    for p in glob.glob(docs + "/**/*.md", recursive=True):
        try:
            head = open(p, errors="replace").read(2000)
        except Exception:
            continue
        m = re.search(r"^offline_minutes:\s*(\d+)", head, re.M)
        if m:
            out.append((os.path.relpath(p, docs), int(m.group(1))))
    return sorted(out)


# --------------------------------------------------------------- main

def main():
    args = sys.argv[1:]
    show_sessions = "--sessions" in args
    include_meta = "--include-meta" in args
    no_global = "--no-global" in args
    global WRITING_BLOCKS
    WRITING_BLOCKS = arg_of(args, "--writing-blocks") or WRITING_BLOCKS
    root, roots, base, audit = resolve_config(args)
    a = parse_local(arg_of(args, "--from") or "") if arg_of(args, "--from") else None
    b = parse_local(arg_of(args, "--to") or "") if arg_of(args, "--to") else None
    docs = os.path.join(root, "docs")
    filt = re.compile(args[args.index("--filter") + 1], re.I) if "--filter" in args else None
    pathrx = re.compile(args[args.index("--paths") + 1], re.I) if "--paths" in args else None
    share = float(arg_of(args, "--share") or 0.4)

    print("== configuración")
    print("  repo auditado : %s" % root)
    print("  raíces (cwd)  : %s" % ", ".join(roots))
    print("  bitácoras     : %s" % base)
    if a or b:
        print("  ventana       : %s -> %s"
              % (local(a).strftime("%Y-%m-%d %H:%M") if a else "inicio",
                 local(b).strftime("%Y-%m-%d %H:%M") if b else "fin"))

    stats = collections.Counter()
    by_sid, meta = load_records(base, roots, a, b, stats)

    # --- pasada de eco: qué líneas de los prompts ya existían antes ese día
    cand = collections.defaultdict(dict)
    for sid, recs in by_sid.items():
        for day, d in prompt_candidates(recs).items():
            for k, ts in d.items():
                prev = cand[day].get(k)
                if prev is None or ts < prev:
                    cand[day][k] = ts
    echoed = scan_echoes(cand, project_dirs(), a, b)
    stats["echoed_lines"] = len(echoed)

    # Mapa del reloj vivo de TODAS las sesiones de TODOS los proyectos: es lo
    # que le dice a la escritura qué instantes estaban libres.
    # El mapa se extiende un día antes de la ventana: si se recortara en `a`,
    # todo lo anterior parecería libre y la escritura se iría a ocuparlo.
    segs = segment_owners(collect_live(
        project_dirs(), a - datetime.timedelta(days=1) if a else None, b))
    stats["live_segments"] = len(segs)

    sessions, meta_sessions, empty = [], [], []
    for sid, recs in by_sid.items():
        s = credit_session(sid, recs, meta, echoed, segs)
        if not s:
            empty.append((sid, title_of(sid, meta), len(recs)))
            continue
        (meta_sessions if sid in audit else sessions).append(s)
    if include_meta:
        sessions += meta_sessions
        meta_sessions = []
    sessions.sort(key=lambda s: s["start"])
    if filt:
        sessions = [s for s in sessions
                    if filt.search("%s|%s|%s" % (s["title"], s["branch"],
                                                 " ".join(s["branches"])))]
    if pathrx:
        keep = []
        for s in sessions:
            hit = sum(v for p, v in s["paths"].items() if pathrx.search(p))
            s["path_share"] = hit / s["n_paths"] if s["n_paths"] else 0.0
            if s["n_paths"] and s["path_share"] >= share:
                keep.append(s)
        sessions = keep
        print("(bucket por rutas: %d sesiones con >=%.0f%% de archivos "
              "coincidentes)" % (len(sessions), share * 100))

    print("\n== insumos")
    print("  sesiones con crédito: %d | de la auditoría: %d | vacías descartadas: %d"
          % (len(sessions), len(meta_sessions), len(empty)))
    print("  registros con timestamp: %d | conservados: %d | duplicados por uuid: %d"
          % (stats["records_with_ts"], stats["records_kept"], stats["dup_uuid"]))
    print("  descartados por cwd ajeno: %d | líneas de prompt detectadas como pegadas: %d"
          % (stats["excluded_foreign_cwd"], stats["echoed_lines"]))
    spill = sum(s.get("writing_spill_h", 0.0) for s in sessions)
    print("  segmentos de reloj vivo: %d | escritura que no cupo antes del corte "
          "de día: %.2f h" % (stats["live_segments"], spill))
    if empty:
        print("  vacías: %s" % ", ".join("%s(%s)" % (s[:8], t[:22]) for s, t, _ in empty))

    ours = os.path.basename(base)
    tr_ours = [t for s in sessions for t in s["tramos"]]
    _, fused_ours = fuse(tr_ours)
    kept = {s["sid"] for s in sessions}
    buckets = {ours: dict(tramos=fused_ours,
                          ts=sorted(d["_ts"] for sid, rs in by_sid.items()
                                    if sid in kept for d in rs),
                          spans=[(s["start"], s["end"]) for s in sessions])}
    tot_intra = sum((min(y, b) - max(x, a if a else x)).total_seconds() * r
                    for x, y, r in fused_ours
                    if (not b or x < b) and (not a or y > a)) / 3600.0 \
        if (a or b) else \
        sum((y - x).total_seconds() * r for x, y, r in fused_ours) / 3600.0
    tot_sess = sum(s["credited_h"] for s in sessions)
    told = sum(s["old_h"] for s in sessions)

    alloc = None
    notes = []
    if not no_global:
        print("\n== línea de tiempo global (todos los proyectos)")
        buckets.update(foreign_buckets(base, roots, a, b, segs))
        alloc_raw, fused_all, per_sess_alloc = allocate(
            buckets, a, b, attribute=(ours, sessions))
        alloc, notes = apply_caps(alloc_raw, buckets, a, b)
        print("  proyectos con actividad en la ventana: %d" % len(buckets))
        print("  %-34s %8s %8s %8s" % ("proyecto", "reloj", "reparto", "topado"))
        for k in sorted(alloc, key=lambda x: -alloc[x]):
            if alloc[k] < 0.01:
                continue
            print("  %-34s %8.2f %8.2f %8.2f%s"
                  % (k[:34], union_hours(buckets[k]["spans"], a, b),
                     alloc_raw.get(k, 0.0), alloc[k],
                     "  <-- ESTE" if k == ours else ""))
        print("  crédito fusionado global (cada instante una vez): %.2f h" % fused_all)
        print("  suma de créditos por proyecto sin reparto: %.2f h"
              % sum(sum((y - x).total_seconds() * r for x, y, r in buckets[k]["tramos"])
                    / 3600.0 for k in buckets))
        for n in notes:
            print("  AVISO %s" % n)

    if alloc:
        raw = alloc_raw.get(ours, 0.0)
        cap_factor = (alloc.get(ours, raw) / raw) if raw else 1.0
        attribute_sessions(sessions, per_sess_alloc, cap_factor)
        # Cierre de caja: bajar a sesiones no puede mover los totales.
        for label, got, want in (
                ("fusión intra-proyecto", sum(s["fused_h"] for s in sessions), tot_intra),
                ("reparto del proyecto", sum(s["allocated_h"] for s in sessions),
                 alloc.get(ours, 0.0))):
            if abs(got - want) > 0.01:
                print("  AVISO descuadre al bajar a sesiones (%s): %.4f vs %.4f"
                      % (label, got, want))

    per = month_breakdown(fused_ours)
    old_per = collections.Counter()
    for s in sessions:
        old_per[s["month"]] += s["old_h"]
    print("\n== horas por mes (America/Mexico_City, corte %02d:00)" % DAY_CUT)
    print("  %-9s %9s %9s %9s" % ("mes", "crédito", "x sesión", "viejo20"))
    per_sess = month_breakdown([t for s in sessions for t in s["tramos"]])
    for m in sorted(set(per) | set(old_per)):
        print("  %-9s %9.1f %9.1f %9.1f" % (m, per[m], per_sess[m], old_per[m]))
    print("  %-9s %9.1f %9.1f %9.1f" % ("TOTAL", tot_intra, tot_sess, told))
    final = alloc.get(ours, tot_intra) if alloc else tot_intra
    print("\n== resultado del proyecto")
    print("  suma por sesión                : %7.2f h" % tot_sess)
    print("  fusión intra-proyecto          : %7.2f h" % tot_intra)
    if alloc:
        print("  reparto global + tope 95%%      : %7.2f h" % final)
    print("  a %.0f MXN/h                  : %s MXN" % (RATE_AI, f"{final*RATE_AI:,.0f}"))

    ms = collections.Counter()
    for s in sessions:
        for k, v in s["mode_split"].items():
            ms[k] += v / 3600.0
    print("\n== reparto del tiempo de máquina por permissionMode (h de reloj)")
    for k, v in ms.most_common():
        print("  %-18s %7.1f" % (k, v))

    off = offline_minutes(docs) if os.path.isdir(docs) else []
    if off:
        print("\n== offline declarado en docs/")
        for p, m in off:
            print("  %-55s %4d min" % (p, m))
        print("  total offline: %.1f h  (%s MXN)"
              % (sum(m for _, m in off) / 60.0,
                 f"{sum(m for _, m in off)/60.0*RATE_AI:,.0f}"))

    if meta_sessions:
        print("\n== sesiones de la propia auditoría (excluidas del total)")
        for s in sorted(meta_sessions, key=lambda x: x["start"]):
            print("  %-40s %6.1f h crédito" % (s["title"][:40], s["credited_h"]))

    if show_sessions:
        print("\n== sesiones")
        print("  %-10s %-40s %7s %7s %7s %7s %6s %6s %6s %7s"
              % ("mes", "título", "crédito", "fusion", "asignad", "span",
                 "escr", "lect", "maq", "pegado"))
        for s in sessions:
            print("  %-10s %-40s %7.2f %7.2f %7.2f %7.2f %6.2f %6.2f %6.2f %7d%s"
                  % (s["month"], s["title"][:40], s["credited_h"],
                     s.get("fused_h", 0.0), s.get("allocated_h", 0.0),
                     s["span_h"], s["writing_h"], s["reading_h"], s["machine_h"],
                     s["pasted_chars"], " *piso" if s["floored"] else ""))

    out = os.path.join(HERE, arg_of(args, "--out") or "credit.json")
    dump = []
    for s in sessions:
        r = {k: v for k, v in s.items() if k != "tramos"}
        r["paths"] = dict(s["paths"].most_common(25))
        r["start"] = s["start"].isoformat()
        r["end"] = s["end"].isoformat()
        dump.append(r)
    json.dump(dict(project_root=root, base=base,
                   window=[a.isoformat() if a else None, b.isoformat() if b else None],
                   sessions=dump, months=dict(per),
                   months_per_session=dict(per_sess),
                   total_per_session_h=tot_sess,
                   total_fused_h=tot_intra,
                   total_allocated_h=final,
                   allocation=alloc, cap_notes=notes,
                   empty_sessions=[dict(sid=s, title=t, n=n) for s, t, n in empty],
                   offline=off, stats=dict(stats)),
              open(out, "w"), indent=1)
    print("\n-> %s" % out)


if __name__ == "__main__":
    main()
