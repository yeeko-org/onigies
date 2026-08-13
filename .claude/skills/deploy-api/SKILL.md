---
name: deploy-api
description: "[api] Deploy the Django API to production (Yeeko server): pre-deploy migration-drift checklist, server runbook (pull, backup, migrate, seeds, gunicorn reload) and post-deploy smoke tests. Use whenever deploying the API, pushing the production branch, running migrations on the server, or debugging a 500 that appeared right after a deploy."
---

# deploy-api

Runbook for deploying `api/` to production (`apionigies.yeeko.org`, Yeeko server). Topology and hosting live in the `deployment` skill; this skill is the procedure.

## Branch discipline

`production` is always **strictly behind `main`** and only advances with `git merge --ff-only` (never cherry-picks) — see `docs/decisions/adr-0001-flow-primero-fast-forward.md`. Commits meant for production go first on `main`; the fast-forward point is the last of them.

When the working tree is dirty (e.g. `.claude/settings.local.json`), skip the checkout: `git push origin main:production` fast-forwards the remote directly, then `git branch -f production origin/production` realigns the local branch.

**A model change and its migration must land in the same commit.** A field committed without its migration poisons every later commit as a deploy target until the migration lands (see incident below).

## Pre-deploy checklist (local)

1. `pytest` green on the ref to deploy.
2. **Migration-drift check** — for the range being deployed:

   ```bash
   git diff --stat <deployed-ref>..<target-ref> -- '*/models.py' '*/migrations/'
   ```

   Any `models.py` change without an accompanying migration in the same range is a stop-the-line signal. Do NOT trust local `pytest` or `makemigrations --check` run from the working tree for this: they see migration files on disk even when those files sit on the wrong side of the branch cut.

   > **Incident 2026-07-29:** `Observable.reach_instances_question` was committed in June without its migration; the migration arrived a month later in a commit excluded from production. The deploy passed pytest and a root-URL smoke test, then every endpoint touching `Observable` returned 500 (`UndefinedColumn`). See `docs/records/2026-07-29-incidente-500-migracion-faltante.md`.

3. **Amended-migration check** — if the range being deployed *modifies* an existing migration file instead of adding a new one, verify on the server that it has not already run:

   ```bash
   psql ... -c "SELECT app, name FROM django_migrations WHERE app='survey';"
   ```

   A migration already recorded there will **not** re-run: the amended operations never touch the schema, `migrate` says nothing and `makemigrations --check` still reports "No changes detected" (it compares models against migration *files*, not against the database). The schema diverges in silence — old columns still alive, new fields missing. Amending is only safe while nothing is deployed; if the row is already there, the fix is manual DDL or a follow-up migration, and it is decided with Ricardo before touching anything.

4. If the frontend also changes: push order matters. Pushing `production` triggers the Netlify build (~2-3 min). Safe direction is **new API + old frontend**; if the skew window matters, lock publishing in the Netlify UI (Deploys → "Lock to stop auto publishing"), deploy the API, then unlock. When the change breaks in **both** directions (frontend and API each need the other's new version), no order is safe — accept the window and minimize it: push, then run the server runbook immediately in one continuous sequence (~6 min achieved on 2026-08-12).

## Data-writing management commands

Any command in the deploy plan that writes rows (seeds included, migrations aside) requires, **before Ricardo approves it**:

1. **Write inventory** — enumerate every model.column the command writes, read from its code, not from its docstring or from what a past record says about it. The decision is presented with the full inventory, never with just the one risk currently under discussion. A written safety claim («idempotente, re-ejecutable») is a snapshot with an expiry condition: it must be re-verified against today's code, not cited.
2. **Pre/post data probe** — grouped counts over the affected columns (`SELECT <col>, COUNT(*) ... GROUP BY <col>`) taken before the run, with the expected after-counts written down in advance, and compared after. A number in the output means nothing without a prior expectation — that is how a damage fingerprint reads as success.
3. **Re-runnable commands follow the `repair_sent_at` pattern** (`api/flow/management/commands/repair_sent_at.py`): dry-run by default, explicit `--apply`, filters that only touch uninitialized rows. Never an unconditional write from a source that stopped being authoritative.

> **Incident 2026-08-12:** re-running `migrate_flow_data` (retired since) silently reset 179 advanced flow statuses to their frozen legacy values — no FlowEvents, smoke all green. The deploy decision had assessed only comment resurrection; the status branch was never enumerated. Its own output carried the fingerprint («1 reconciliación bp_draft → bp_completed») and was read as success. See `docs/records/2026-08-12-incidente-migrate-flow-data.md`.

## Server runbook

SSH: `ssh -i ~/.ssh/servers/yeeko.pem ubuntu@api.yeeko.org` — repo at `~/unam/onigies`, venv at `api/venv`, passwordless sudo.

```bash
cd ~/unam/onigies && git status --short     # 1. working tree must be clean
cd api && mkdir -p _backups                 # 2. backup before schema changes
# pg_dump -Fc with the .env creds (lines carry \r — read them with tr -d '\r'),
# or take an RDS snapshot instead for big changes
git pull origin production                  # 3. bring the code
venv/bin/pip install -r requirements.txt    # 4. only if requirements changed
venv/bin/python manage.py migrate           # 5. schema
venv/bin/python manage.py makemigrations --check --dry-run   # 6. MUST say "No changes detected" — if not, do NOT reload; a model shipped without its migration
# 7. idempotent seeds if their source changed: seed_flow, migrate_ps_schemas
#    question/seed_data/ changed → load_sectors, then
#    load_questionnaire --sync-institutions (backfills the new wrappers).
#    load_sectors FIRST: load_questionnaire aborts with "Sectores
#    inexistentes" if a sector it references is missing (deploy 2026-08-04).
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
