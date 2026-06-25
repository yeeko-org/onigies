---
name: bp-validation-ux
description: How the Buenas Prácticas validation UX/UI is laid out for the two
  audiences — the IES (institution, in /respuestas) and the reviewer (revisora,
  in /dashboard). Use when touching the good-practice review screens, the
  GoodPracticePackage (Envío de Buenas Prácticas) detail, scoring/calificación of
  features, the GoodPracticeCard/GoodPracticeEditSimple components, or deciding
  what each audience may see and edit. Covers why the reviewer detail lives in an
  EditSimple, why there is an empty Sheet, and how the calificación is kept
  private from the IES.
---

# bp-validation-ux

Two audiences review the **same** bp models from two surfaces. Keep them
separate — the rule is the status `role` (whose turn it is) from the
[`flow`](../flow/SKILL.md) engine, never a hardcoded status name.

| Audience | Route | Entry component | What they do |
|---|---|---|---|
| **IES** (institution) | `/respuestas/[period]` | `GoodPracticeList.vue` | answer `has_good_practices`, write/edit each práctica, mark features, send the envío to review |
| **Revisora** (reviewer, staff) | `/dashboard` → colección "Envíos de buenas prácticas" | `GoodPracticePackageEditSimple.vue` | score (calificar) each práctica's features, rule each one's status, finish the envío |

Naming: it is an **"Envío de Buenas Prácticas"**, never "paquete" (the model is
still `GoodPracticePackage`; only code keeps that name). The collection name is
set in `api/example/catalog_schema.py` (`GoodPracticePackageSchema`).

Models, the status catalog, transitions, propagation and the per-practice
`FlowStatusActions`/`FlowComments` plumbing all belong to the
[`flow`](../flow/SKILL.md) skill — this skill is only the **layout and
audience split**.

## The shared building blocks (reused by both surfaces)

| Component | Role | Audience knob |
|---|---|---|
| `example/good_practice/GoodPracticeCard.vue` | compact summary of one práctica (axes, evidence count, status chip) | `isStaff` → reviewer adds "X/Y evaluados"; clickable/"Evaluar" when `isStaff` even off-turn |
| `example/good_practice/GoodPracticeEditSimple.vue` | the práctica detail opened in a **dialog** (content + features + status + comments) | `isStaff` → reviewer sees content read-only + scoring; `editable` → may edit now |
| `example/good_practice/FeatureList.vue` + `FeatureItem.vue` | the características: IES marks (`has_attribute`/justification/evidences), reviewer scores (`final_option` slider) | `isStaff` chooses mode; `editable` gates editing by turn |

Two distinct knobs, do not conflate them:

- **`isStaff`** = *which audience* → IES marking mode vs reviewer scoring mode.
- **`editable`** = *may this user edit now* → read-only when false. One prop name
  across `GoodPracticeCard`, `GoodPracticeEditSimple` and `FeatureList`, but each
  surface computes it differently:
  - **IES** (`GoodPracticeList`): `canEdit(obj) = !isStaff &&
    flowStore.canEditContent(obj, goodPracticePackage)` — **root-aware, per
    práctica**. Editing depends on the **envío (root)** being in the IES's turn
    *plus* the práctica's own `content_editable` (the two-permissions model — see
    [`flow`](../flow/SKILL.md)). Once the envío is sent, every práctica is
    read-only even if its own status is an IES-turn one.
  - **Revisora** (`GoodPracticePackageEditSimple`): `canReview =
    flowStore.getStatus(pkg.status)?.role === 'reviewer'` — package-level and
    uniform, passed as `:editable` to all cards/dialog. Live only in
    `bp_sent`/`bp_resent`.

## IES surface — `GoodPracticeList.vue` (`/respuestas`)

- Owns the IES-only question `has_good_practices` (orthogonal to the flow — a
  boolean, not a status). The Sí/No radio, "Cambiar respuesta", send/discard/
  reopen all live here; see [`flow`](../flow/SKILL.md) for `discard`/`reopen`.
- Renders a grid of `GoodPracticeCard` (`isStaff=false`); clicking opens
  `GoodPracticeEditSimple` in a `v-dialog` to edit content and mark features.
- "Enviar a revisión" runs the package transition `bp_sent` via `useFlow`; the
  motor blocks it until every práctica is `bp_completed` (children rule).
- The IES **never** sees the calificación (see "Calificación privacy" below).

## Revisora surface — `GoodPracticePackageEditSimple.vue` (`/dashboard`)

This is the reviewer's single control center. It is an **`EditSimple`**, so the
dashboard auto-loads it inline for the `GoodPracticePackage` collection with
**only** `v-model` (see [`dashboard-collections`](../dashboard-collections/SKILL.md)
§2 for the convention). It deliberately mirrors `GoodPracticeList.vue`:

1. **Header** — institución / período / `sent_at` chips + `FlowComments` +
   `FlowStatusActions` of the envío (`model-name="goodpracticepackage"`) + a
   "X/Y dictaminadas" progress chip (`ruledCount` = practices whose status
   `role === null`, i.e. terminal `bp_for_ruling`/`bp_rejected`).
2. **`canReview`** = `flowStore.getStatus(pkg.status)?.role === 'reviewer'`
   (true in `bp_sent`/`bp_resent`). It is passed down as `editable`, so
   scoring and the "Evaluar" button are live only on the reviewer's turn;
   otherwise everything is read-only (the reviewer can still open a práctica to
   look).
3. **Grid** of `GoodPracticeCard` (`isStaff=true`, `:editable="canReview"`)
   over `pkg.good_practices`.
4. **Dialog** — clicking a card opens `GoodPracticeEditSimple`
   (`isStaff=true`, `:editable="canReview"`) where the reviewer scores
   (`FeatureList`) and runs the práctica's own `FlowStatusActions`.

### Open the dialog with the nested object directly (no extra fetch)

`GoodPracticePackageFullSerializer` nests each práctica with the **full**
`GoodPracticeFullSerializer` (`feature_values`, `evidences`, `flow_events`,
`status`) — `api/api/views/example/serializers.py`. So `openPractice` sets
`editingPractice` to the **same object reference** from
`pkg.good_practices`; mutating its `status`/`flow_events`/`feature_values` in
the dialog refreshes the card with no reload (unlike the IES list, which
re-fetches). This is a deliberate simplification.

### Why the empty `GoodPracticePackageSheet.vue`

In `PanelCommon.vue` the dashboard renders the `EditSimple` **and**, always
below it, the `#sheet` slot — which `PanelList` fills with the resolved
`{Model}Sheet` (fallback `SheetCommon` → the child-collection list, see
[`dashboard-collections`](../dashboard-collections/SKILL.md) §5). Without an
override that auto-list would render `good_practices` a **second** time, below
the curated list, with its filter/search/pagination/massive-edit bar — the mess
this redesign removed. `GoodPracticePackageSheet.vue` exists and **renders
nothing**, so `useDynamicComponent` prefers it over `SheetCommon` and the
duplicate list disappears. Keep it; deleting it brings the duplicate back.

## Calificación privacy — the IES must never see the score

The calificación is **reviewer-only**: `FeatureGoodPractice.final_option`
(the slider score), its reviewer `comments` and `reviewers`, plus the rollup
`GoodPractice.final_value`. The IES sees only its own marking
(`has_attribute`/`justification`/`evidences`) and the **status**.

Enforced at two layers — keep both:

1. **UI** — in `FeatureItem.vue` the scoring block (slider, "Evaluado" chip,
   reviewer Comments) is behind `v-if="isStaff"`; in `GoodPracticeCard.vue` the
   "X/Y evaluados" chip is `v-if="isStaff"`. The IES passes `isStaff=false`, so
   it is not rendered.
2. **Payload** — UI hiding alone still ships the fields over the wire. The
   serializer drops them in `to_representation` via the helper
   `hide_review_fields(serializer, data, names)` in
   `api/api/views/example/serializers.py`, gated on `request.user.is_reviewer`
   (= superuser ∨ staff ∨ `reviewer` flag — `ies.User.is_reviewer`).
   `FeatureGoodPracticeSerializer` drops `['final_option', 'comments',
   'reviewers']`; `GoodPracticeSerializer` drops `['final_value']`. It runs in
   `to_representation` (not `__init__`) so it works for the **nested**
   `feature_values` too — DRF propagates `context` to any depth, while a
   declared nested serializer's `__init__` runs at import time with no request.

This is read-only protection. The fields stay writable server-side; the IES has
no UI to set them, but if strict write-locking is needed, gate it separately.

## Key files

| Concern | File |
|---|---|
| Reviewer control center | `nuxt/.../example/good_practice_package/GoodPracticePackageEditSimple.vue` |
| Empty Sheet (suppress dup list) | `nuxt/.../example/good_practice_package/GoodPracticePackageSheet.vue` |
| IES list | `nuxt/.../example/good_practice/GoodPracticeList.vue` |
| Práctica card (both) | `nuxt/.../example/good_practice/GoodPracticeCard.vue` |
| Práctica dialog detail (both) | `nuxt/.../example/good_practice/GoodPracticeEditSimple.vue` |
| Feature scoring/marking | `nuxt/.../example/good_practice/FeatureList.vue`, `FeatureItem.vue` |
| Payload privacy + serializers | `api/api/views/example/serializers.py` |
| Collection name / schema | `api/example/catalog_schema.py` |
| Status engine, roles, transitions | skill [`flow`](../flow/SKILL.md) |
| EditSimple/Sheet auto-load convention | skill [`dashboard-collections`](../dashboard-collections/SKILL.md) |