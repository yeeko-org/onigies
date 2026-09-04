---
name: deployment
description: Deployment topology, hosting, and the migration roadmap for the ONIGIES monorepo. Use when touching nginx config, the UNAM or Yeeko servers, the temporary Netlify bridge, environment variables, production setup, DNS, or when asking what is left to migrate or deploy.
---

# deployment

How the ONIGIES monorepo is hosted **during the transition** from the legacy system to the new stack. This setup is temporary: it exists until the UNAM virtual machine is provisioned.

## Topology

```
Browser at onigies.unam.mx/dashboard
   │
   ├─ HTML + /_nuxt/  ──► nginx (UNAM) ──proxy──► onigies.netlify.app   new frontend
   │
   └─ /api/... · /files/... ───────────────────► apionigies.yeeko.org   new backend
                                                  cross-origin · token in header

onigies.unam.mx/ · /api · /admin · /media · /static
   └─► nginx (UNAM) ──► legacy Django 127.0.0.1:6000   legacy public site
```

The new dashboard is a **self-contained stack** — frontend on Netlify, API on Yeeko. How the Netlify build runs, its lockfile, and how to verify a publication live in the `deploy-api` skill (section «Frontend build on Netlify»). The nginx bridge only forwards the frontend; it never touches the API. The dashboard behaves identically at `onigies.netlify.app` or `onigies.unam.mx` because `NUXT_API_URL` is baked into the build.

## Hosts

| Component | Runs on | Public URL |
|---|---|---|
| Legacy public site (Vue 2) | UNAM server — static `/var/www/onigies/` | `onigies.unam.mx/` |
| Legacy backend (Python 2 Django) | UNAM server — `127.0.0.1:6000` | `onigies.unam.mx/{api,admin,media,static}` |
| New dashboard (`nuxt/`) | Netlify | `onigies.netlify.app`, bridged onto `onigies.unam.mx` |
| New API (`api/`) | Yeeko server | `apionigies.yeeko.org` |

Netlify build env vars (baked at build time, so the browser always calls Yeeko):

```
NUXT_API_URL=https://apionigies.yeeko.org/api
NUXT_ADMIN_URL=https://apionigies.yeeko.org/admin
```

## The temporary nginx bridge

Lives in the UNAM server's nginx site config (e.g. `/etc/nginx/sites-available/onigies.unam.mx`). Two `location` blocks forward the dashboard's six routes and the Nuxt build assets to Netlify; the legacy `location` blocks (`/`, `/api`, `/admin`, `/media`, `/static`) stay untouched.

```nginx
# Dashboard pages → Netlify
location ~ ^/(dashboard|respuestas|login|register|forgot-password|recover-password)(/|$) {
        proxy_pass https://onigies.netlify.app;
        proxy_ssl_server_name on;
        proxy_set_header Host onigies.netlify.app;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_redirect https://onigies.netlify.app/ /;
}

# Nuxt build assets (JS/CSS) → Netlify
location /_nuxt/ {
        proxy_pass https://onigies.netlify.app;
        proxy_ssl_server_name on;
        proxy_set_header Host onigies.netlify.app;
}
```

Why the non-obvious directives:

| Directive | Reason |
|---|---|
| `Host onigies.netlify.app` | Netlify is multi-tenant and routes by `Host`. The real host returns "site not found". |
| `proxy_ssl_server_name on` | Sends SNI in the TLS handshake so Netlify serves the right certificate. |
| `location /_nuxt/` | Build assets use absolute paths; without proxying them the browser hits the legacy site and gets its `index.html`. |
| no URI after `proxy_pass` | In a regex `location`, a URI part in `proxy_pass` is a syntax error; omitting it forwards the path verbatim. |

Apply on the server:

```bash
sudo cp /etc/nginx/sites-available/onigies.unam.mx{,.bak}
sudo nginx -t                  # validate syntax
sudo systemctl reload nginx    # apply with no downtime
```

Rollback: restore the `.bak` and reload.

## Why no backend change was needed

The dashboard calls `apionigies.yeeko.org` cross-origin, and it works without CORS edits because:

- `api/core/settings/__init__.py` sets `CORS_ORIGIN_ALLOW_ALL = True` — every origin is accepted.
- Auth is a token in the `Authorization` header (`nuxt/app/plugins/api.ts`, no `withCredentials`), so CSRF never triggers.

**Hardening pending:** `CORS_ORIGIN_ALLOW_ALL = True` is wide open. Tighten it to an explicit `CORS_ALLOWED_ORIGINS` allowlist once the topology stabilizes — tracked in the roadmap.

## Uploaded files — private S3 bucket, `/files/` namespace

Production stores user uploads in the private S3 bucket `onigies-v3-temporal`, gated by `USE_S3_FILES=1` in the server `.env` — a bridge until the UNAM server, where files return to disk (`migrate_files_to_s3 --download`); decisions and rationale in `adr-0013`. Flag off (local dev, or rollback) → local-disk behavior returns unchanged; the pre-migration files remain on the EC2 disk as backup. `USE_S3_FILES=1` requires `AWS_STORAGE_BUCKET_NAME` and `AWS_S3_REGION_NAME` in the `.env` (startup fails loudly without them), plus `AWS_LOCATION` and the key pair.

Downloads go through a permission-checked endpoint (`/api/flow/<app>/<model>/<pk>/attachments/<id>/download/`): 302 to an ephemeral signed URL; `?redirect=false` returns it as JSON for the authenticated frontend; `Attachment.is_public=True` opens the file to anonymous users. The open `/files/` route dies automatically when the flag is on (`core/urls.py` guards on `MEDIA_URL` containing `://`). Production currently runs `DEBUG=True` (hardening pending).

The `/files/` namespace survives in S3 as the bucket prefix (`AWS_LOCATION=files`), so `FileField` values in the DB never changed. It was **renamed from `/media/`** to avoid a collision with the legacy site: the UNAM nginx routes `onigies.unam.mx/media/...` to the legacy Django, and some serializers emitted file URLs the browser resolves against the frontend origin. Under the `onigies.unam.mx` bridge, a new-system file referenced as `/media/...` therefore hit the legacy backend and 404'd.

The fix (§5 in `docs/records/2026-06-26-seguimiento-pendientes-ruben.md`):

- `MEDIA_URL = '/files/'`, `MEDIA_ROOT = BASE_DIR/'files'` (`core/settings/__init__.py`).
- `core/urls.py` serves `/files/` with an explicit `re_path(..., django.views.static.serve, ...)` instead of `static()`. `static()` registers no routes when `DEBUG=False`; the explicit route serves **regardless of DEBUG**, so it survives the pending `DEBUG=False` hardening.
- File URLs stay **absolute** via `request.build_absolute_uri` (`flow` now emits the download-endpoint URL; the browser then follows the 302 to S3). The UNAM nginx is never in the path — no `/files/` nginx block is needed.

Cutover on the server (2026-06, flag-off era): the on-disk folder moved `media/` → `files/`. **No DB migration** — `FileField` values are storage-relative (e.g. `evidences/foo.pdf`), so they resolved unchanged against the new root, and later against the S3 prefix.

**Trade-off (applies when the flag is off):** serving media through Django's `serve` view is less efficient than an nginx `alias`. Acceptable at ONIGIES's scale, and deliberate — it keeps file serving out of nginx, so nothing needs reconfiguring when the API moves to the UNAM VM. With S3 on, the browser downloads straight from the bucket and no WSGI worker touches file bytes.

## Migration roadmap

The running checklist of what is left to move onto UNAM infrastructure lives in [`references/roadmap.md`](references/roadmap.md). Update that file as steps land; keep this SKILL.md for the stable runbook.