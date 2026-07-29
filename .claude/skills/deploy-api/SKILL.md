---
name: deploy-api
description: "[api] Deploy the Django API to production (Yeeko server): pre-deploy migration-drift checklist, server runbook (pull, backup, migrate, seeds, gunicorn reload) and post-deploy smoke tests. Use whenever deploying the API, pushing the production branch, running migrations on the server, or debugging a 500 that appeared right after a deploy."
---

# deploy-api

Runbook for deploying `api/` to production (`apionigies.yeeko.org`, Yeeko server). Topology and hosting live in the `deployment` skill; this skill is the procedure.

## Branch discipline

`production` is always **strictly behind `main`** and only advances with `git merge --ff-only` (never cherry-picks) — see `docs/decisiones/0001-flow-primero-fast-forward.md`. Commits meant for production go first on `main`; the fast-forward point is the last of them.

**A model change and its migration must land in the same commit.** A field committed without its migration poisons every later commit as a deploy target until the migration lands (see incident below).

## Pre-deploy checklist (local)

1. `pytest` green on the ref to deploy.
2. **Migration-drift check** — for the range being deployed:

   ```bash
   git diff --stat <deployed-ref>..<target-ref> -- '*/models.py' '*/migrations/'
   ```

   Any `models.py` change without an accompanying migration in the same range is a stop-the-line signal. Do NOT trust local `pytest` or `makemigrations --check` run from the working tree for this: they see migration files on disk even when those files sit on the wrong side of the branch cut.

   > **Incident 2026-07-29:** `Observable.reach_instances_question` was committed in June without its migration; the migration arrived a month later in a commit excluded from production. The deploy passed pytest and a root-URL smoke test, then every endpoint touching `Observable` returned 500 (`UndefinedColumn`). See `docs/historico/2026-07-29-incidente-500-migracion-faltante.md`.

3. If the frontend also changes: push order matters. Pushing `production` triggers the Netlify build (~2-3 min). Safe direction is **new API + old frontend**; if the skew window matters, lock publishing in the Netlify UI (Deploys → "Lock to stop auto publishing"), deploy the API, then unlock.

## Server runbook

SSH: `ssh -i ~/.ssh/servers/yeeko.pem ubuntu@api.yeeko.org` — repo at `~/unam/onigies`, venv at `api/venv`, passwordless sudo.

```bash
cd ~/unam/onigies && git status --short     # 1. working tree must be clean
cd api && mkdir -p _backups                 # 2. backup before schema changes
# pg_dump with the .env creds (same pattern as deploy_flow_migration.sh),
# or take an RDS snapshot instead for big changes
git pull origin production                  # 3. bring the code
venv/bin/pip install -r requirements.txt    # 4. only if requirements changed
venv/bin/python manage.py migrate           # 5. schema
venv/bin/python manage.py makemigrations --check --dry-run   # 6. MUST say "No changes detected" — if not, do NOT reload; a model shipped without its migration
# 7. idempotent seeds if their source changed: seed_flow, migrate_ps_schemas
sudo supervisorctl restart apionigies       # 8. reload (brief downtime, seconds)
```

Reload gotchas (multi-tenant box, ~20 client apps under one supervisord):
- `supervisorctl` needs **sudo** (plain `supervisorctl` fails with `Permission denied` — do not misread it as a missing socket).
- Zero-downtime alternative to restart: `sudo kill -HUP $(pgrep -f "unam/onigies/api/venv/bin/gunicorn" -P $(pgrep -x supervisord))` — reloads workers in place (the master also runs as root).
- **Never** `systemctl restart supervisor` or `supervisorctl stop/restart all` — it takes every client app down. Only ever touch `apionigies` (port `6018`; the old `[program:onigies]` on `:6005` with venv `~/env/onigies` is NOT this app — this app's venv is `~/unam/onigies/api/venv`).

## Post-deploy smoke

A root-URL check proves nothing — hit endpoints that exercise real models:

| Check | Expect |
|---|---|
| `curl https://apionigies.yeeko.org/api/catalogs/all/` | 200 — touches most catalog models; this is the endpoint that exposed the 2026-07-29 incident |
| `curl https://apionigies.yeeko.org/api/` | 200 |
| An evidence file under `/files/evidences/<name>` (ASCII name; accents double-encode through the shell) | 200 |
| `tail ~/unam/logs/onigies_api/error.log` | no new tracebacks |
| Manual: login on the dashboard, open /respuestas and a BP package | works |

Old workers keep serving during the HUP handoff, so a failed smoke means the new code is bad, not a mid-restart blip — fix forward or `git checkout <previous-ref>` + HUP to roll back.
