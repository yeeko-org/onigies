# Migration roadmap

Living checklist for moving the ONIGIES monorepo off the temporary setup and onto UNAM infrastructure. See `../SKILL.md` for the stable deployment runbook.

This is a **skeleton** — correct, reorder, and expand it as the real plan firms up.

_Last updated: 2026-07-29_

## Phase 0 — Temporary bridge (done)

- [x] New API live at `apionigies.yeeko.org` (Yeeko server)
- [x] New dashboard deployed on Netlify (`onigies.netlify.app`)
- [x] nginx on the UNAM server proxies the six dashboard routes + `/_nuxt/` to Netlify
- [x] Uploads served under `/files/` — server cutover `media/` → `files/` done 2026-07-29 (old partial copy kept in `api/_backups/files_stale_jul04`)

## Phase 1 — UNAM virtual machine

- [ ] VM provisioning approved and delivered (trámite in process)
- [ ] Provision the VM: OS, Python, Node + pnpm, PostgreSQL access, nginx
- [ ] Deploy the `api/` backend on the VM
- [ ] Decide where the `nuxt/` app runs long-term (VM vs. stay on Netlify)
- [ ] Repoint `NUXT_API_URL` / `NUXT_ADMIN_URL` to the final API host
- [ ] Replace the nginx bridge with direct serving; remove the Netlify proxy blocks

## Phase 2 — Hardening

- [ ] Replace `CORS_ORIGIN_ALLOW_ALL = True` with an explicit `CORS_ALLOWED_ORIGINS` allowlist
- [ ] Review `ALLOWED_HOSTS` for the production host
- [ ] Confirm `DJANGO_DEBUG=False` in production

## Phase 3 — Legacy retirement

- [ ] Rebuild the public-facing site (currently the 2017–2018 Vue 2 app)
- [ ] Migrate or archive data from the legacy Python 2 Django
- [ ] Retire the legacy Django (`127.0.0.1:6000`) and `/var/www/onigies/`

## Open decisions

- Long-term home of the Nuxt app: UNAM VM, or stay on Netlify with a permanent bridge?
- Final domain layout: keep `apionigies.yeeko.org`, or move the API under `onigies.unam.mx`?