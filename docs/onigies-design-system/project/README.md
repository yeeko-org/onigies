# ONIGIES Design System

**Observatorio Nacional para la Igualdad de Género en las Instituciones de Educación Superior**

A refresh of the ONIGIES brand and product surfaces, marrying **Material Design** (structure, elevation, type hierarchy) with **soft Neumorphism** (sculpted surfaces, paired light/dark shadows on a warm off‑white canvas) — without losing the colorful, institutional voice the observatory needs.

> _Es un observatorio institucional — debe verse serio — pero el tema es género, así que vale la pena que sea amigable._ — brief

---

## Context

ONIGIES is a Mexican observatory that publishes an annual gender‑equality index for Higher‑Education Institutions (IES). It scores institutions on a 0–5 scale per axis and aggregates to a national average.

It has two product surfaces:

1. **Public observatory site** — informational, data‑forward. Index gauge, axis breakdowns, historical comparisons, per‑institution drill‑downs, downloadable reports.
2. **Admin dashboard** — used by ONIGIES staff and IES representatives to upload evidence, manage instrument responses, audit submissions, and publish the annual index.

### What changed

The most important brand change: **the index has been re-organized from 8 ejes into 4 ejes.** That collapses the original 8-color logo wheel into a 4-color brand palette. The 4 official ejes are:

| Eje (largo) | Corto | Color | Material Symbols icon |
|---|---|---|---|
| Igualdad de género | Igualdad | **Morado** `#6E4BC4` | `add` |
| Inclusión y no discriminación | Inclusión | **Azul** `#2E8FCC` | `self_improvement` |
| Cuidados corresponsables | Cuidados | **Amarillo** `#F2A53A` | `baby_changing_station` |
| Una vida libre de discriminaciones y violencias | Vida libre | **Rosa** `#E63E9A` | `volunteer_activism` |

### A 5th color for actions: **Turquesa** (the primary)

The action / brand-primary color used across **both** surfaces is **turquesa** `#14A8A0` — deliberately distinct from the 4 ejes so it never reads as a data tag. It is used for:

- CTAs and primary buttons (Descargar, Suscribirse, Cerrar ciclo y publicar)
- The Índice Global readout and gauge (so it doesn't collide with the morado eje)
- The active state in nav, year picker, year selector
- Focus rings (`--glow-primary`)
- The aggregate row in the IES table ("Todas las IES")

Whenever you see `--brand`, `--primary-500`, `--brand-tint`, you're pulling turquesa.

For the **admin dashboard**, turquesa is again the primary action color; the chrome (sidebar) is anchored in deep **índigo** (`#2C2F6E`) for calmer long-session work, and the 4 eje colors appear only as data tags on evidence cards, score bars, and KPI accents.

---

## Sources reviewed

- `assets/logo-onigies.svg` — the canonical 8‑arm logo, used here only as the brand mark; the new palette is derived from it but not constrained to its exact hexes.
- `assets/octagono.png` — the 8‑axis wheel diagram (informational; not used as‑is in the refresh).
- `assets/reference-current-site.png` — current ONIGIES dashboard. Note the dense KPI grid, the gauge, the histogram, the per‑IES matrix — these layouts are preserved in the refresh.
- `assets/reference-stripe-1.png`, `assets/reference-stripe-2.png` — Stripe.com hero & feature blocks, used as the neumorphism / Material reference. We take the soft pastel gradients, gentle rounded cards, layered window mockups — but we **do not** copy Stripe's blue‑purple gradient washes or its decorative particle illustrations; those are not on‑brand for ONIGIES.

---

## Project index

```
ONIGIES Design System/
├── README.md                     ← you are here
├── SKILL.md                      ← agent skill manifest
├── colors_and_type.css           ← all tokens (colors, type, radii, spacing, shadows, motion)
├── assets/
│   ├── logo-onigies.svg          ← canonical logo
│   ├── octagono.png              ← legacy 8-eje wheel
│   ├── reference-current-site.png
│   ├── reference-stripe-1.png
│   └── reference-stripe-2.png
├── preview/                      ← design-system tab cards
│   ├── 01-logo.html
│   ├── 02-brand-colors.html
│   ├── ...
├── ui_kits/
│   ├── public_site/              ← observatory site (informational)
│   │   ├── README.md
│   │   ├── index.html
│   │   └── *.jsx
│   └── admin_dashboard/          ← internal data-entry / publishing app
│       ├── README.md
│       ├── index.html
│       └── *.jsx
```

---

## CONTENT FUNDAMENTALS

### Voice & tone

ONIGIES is **institutional but warm**. It is read by university rectors, policy researchers, journalists, and students. It must sound credible enough to be cited and human enough to invite engagement.

- **Spanish (México)** is the canonical language. All product copy is Spanish; English is secondary at most.
- **Formal, but not bureaucratic.** Use _usted_ in legal disclaimers and report front-matter; use _tú_ in product UI ("Filtra IES", "Consulta el avance"). Default to **second-person imperative for UI labels** ("Descarga", "Compara", "Consulta").
- **Avoid jargon walls.** Define acronyms on first use: "Instituciones de Educación Superior (IES)". Never assume the reader knows what an _eje_ is — explain it in one short sentence.
- **No emoji.** Emoji conflict with the institutional register. The colorful logo and palette carry the warmth.
- **Inclusive language by default.** Where it doesn't make the sentence brittle, use neutral forms: "la población estudiantil" over "los estudiantes", "el personal académico" over "los profesores". Avoid the _-e/-x_ neologisms in flagship copy; the institutional context still expects standard Spanish.
- **Numbers carry weight.** A single number like _"2.0 de 5"_ or _"48 IES"_ should usually be the largest thing on the screen — bigger than its label.

### Casing & punctuation

- **Sentence case** for headings, buttons, and labels: "Descarga de resultados", "Resultados de las 48 IES" — never Title Case.
- **ALL-CAPS** is reserved for the overline label of a section (e.g. `EJES`, `BLOG` in the nav) and for the institution acronym list (BUAP, CIAD, Cinvestav). Use sparingly with `letter-spacing: 0.12em`.
- **Spanish punctuation:** opening `¿` `¡` on questions/exclamations. Use _comillas latinas_ «…» in long-form content, regular `"…"` is acceptable in product UI.
- **Numbers:** Spanish locale — `2,010,569,010` style; decimal is a point in indices ("2.0 de 5") because the original index uses dot decimals. Be consistent within a screen.

### Copy examples that pass / fail

| ✅ On-brand | ❌ Off-brand |
|---|---|
| "Consulta el avance de cada IES en igualdad de género." | "Click here to see the data!" |
| "Descarga el Informe 2026 en formato PDF." | "📥 Get the report 🚀" |
| "BUAP avanzó 0.3 puntos respecto al año anterior." | "BUAP went up a bit this year." |
| "Aún no tenemos datos para esta institución." | "Oops! No data found 😅" |
| "Filtra IES por estado, tipo o avance." | "🔍 Search the data" |

### Structural conventions

- Big number first, label second, supporting context third.
- Use the eje icon + eje color as the visual carrier for "what topic is this about?" — never carry that role in body copy alone.
- When linking out to the methodology or to a downloadable report, use a `↓` (descargar) or `→` (leer más) suffix, never an emoji.

---

## VISUAL FOUNDATIONS

### The hybrid: Material + Neumorphism

| | Material Design provides | Soft Neumorphism provides |
|---|---|---|
| **Structure** | type scale, 4px grid, elevation tiers, ripple feedback on tap | — |
| **Surface treatment** | white cards with crisp shadows for floating UI (menus, dialogs, toasts) | warm-gray sculpted surfaces for stationary UI (KPI tiles, score discs, toggles, inputs) |
| **Color** | tonal palettes (50→900), semantic roles | — |
| **Friendliness** | — | the soft "pressed-foam" feel; the inset wells, the gentle drop shadows |

**Rule of thumb:** if it _floats above_ the page (menu, modal, dropdown, toast) → Material elevation (`--elev-3` / `--elev-4`). If it _is_ the page (KPI tile, score disc, axis card, toggle, input) → Neumorphism (`--neu-raised` / `--neu-inset`).

### Color usage

- The page background is **always `--bg-page`** (`#F6F4F9`). This warm off-white is what makes neumorphic shadows work. Never put neumorphic cards on pure white.
- Use brand color as an **accent**, not as a background, except in two places:
  1. Large promotional/hero cards (one big card, full bleed of one brand color, white text).
  2. Eje-tagged data (the axis chip, the score disc fill, the table row indicator).
- Never combine all four brand colors in one component at the same weight — pick one as primary, others as 100/50 tints.
- For the **admin dashboard** the chrome is `--indigo-700` with `--turquesa-500` accents; brand colors appear only as data tags.

### Type

- **Plus Jakarta Sans** for everything display/heading. Geometric, slightly humanist, friendly without being playful.
- **Manrope** for body and UI. Round terminals echo the neumorphic curves.
- **JetBrains Mono** for tabular code/IDs (e.g. submission IDs in the admin).
- Headings always **`-0.015em` to `-0.02em`** tracking; body is neutral.
- **Tabular numerals** (`font-variant-numeric: tabular-nums`) on every number that sits in a column.

> Substitution note: ONIGIES did not supply brand fonts. Plus Jakarta Sans + Manrope are Google Fonts substitutions chosen to match the friendly-institutional register. **Please confirm with the ONIGIES communication team** whether to keep these or swap for licensed fonts.

### Spacing & layout

- 4px base grid; primary stops are 4/8/12/16/24/32/40/56/72/96.
- Page gutters: 24px (mobile) → 32px (tablet) → 48px (desktop) → 64px (≥1440).
- Cards have **at least 24px** internal padding; large feature cards 32–40px.
- Maximum content column width 1240px on the public site; admin dashboard goes full bleed with a fixed 248px sidebar.

### Corner radii

Generous, but not pill-shaped except for chips/buttons-as-tags:
- inputs & buttons → 12px
- standard card → 16px
- large hero card or KPI disc container → 22px
- modal / sheet → 24–32px
- chips, score badges → pill (full radius)

### Shadow systems (used together)

- **Material elevation:** `--elev-1` to `--elev-5`. Single drop, neutral. Use for floating UI.
- **Neumorphism:** `--neu-raised`, `--neu-raised-sm`, `--neu-raised-lg`, `--neu-inset`, `--neu-inset-sm`. Paired light+dark. Use for stationary UI.
- **Color glow** (`--glow-rosa` etc.) — used for focus rings and the "currently selected" KPI tile.

The light source is fixed top-left across the system. Do not flip neumorphic shadows.

### Backgrounds & imagery

- The signature decorative element is a **soft pastel gradient wash** — a single oklch blend (e.g. ámbar → rosa, or violeta → azul) at low saturation, used as a hero backdrop. This is the one thing borrowed directly from the Stripe references. Always blurred / grainy, never sharp.
- We do **not** use particle-cloud illustrations, isometric 3D, or photographic faces of real people. ONIGIES is data-first; imagery is restrained.
- Where a hero needs a "thing", use a tilted screenshot of the index dashboard (similar to Stripe's "browser inside the hero") rather than abstract art.
- Card backgrounds: solid (`--bg-surface-raised` white for Material cards, `--bg-page` for neumorphic cards). No textures.

### Hover & press states

- **Buttons** (filled): hover = darken brand by one step (e.g. 500 → 600), shadow steps up `--elev-1 → --elev-2`. Press = darken to 700, shadow drops to inset.
- **Cards** (clickable): hover = lift shadow `--neu-raised → --neu-raised-lg` + 1px upward translate. Press = inset `--neu-inset`.
- **Icon buttons / tabs**: hover = `--neutral-100` background ring. Press = inset.
- **Links**: underline on hover, color stays `--fg-link`.
- All transitions: `var(--dur-base) var(--ease-out)` — 220ms cubic-bezier(0.22, 1, 0.36, 1).

### Motion

- Page-level: fade + 8px translate, 360ms ease-out.
- Card hover: 220ms ease-out.
- Modal/sheet open: spring (`--ease-spring`), 320ms.
- KPI number changes: tween from old value to new over 600ms, ease-in-out.
- **No bouncing decorative animations**; we are an institution.

### Borders

Borders are used sparingly because shadows do most of the work. When used:
- 1px `--border-soft` for dividers inside cards.
- 1px `--border-medium` for input rest states.
- 2px brand color for active tabs and focused inputs (paired with `--glow-*`).

### Transparency & blur

- Used on the **top app bar** when scrolled (white at 70% opacity, 16px backdrop-blur).
- Used on **modal scrims** (`rgba(20,19,27,0.45)` with 6px blur).
- Avoid translucent cards over photography — there is no photography to begin with.

### Card anatomy (canonical)

A standard ONIGIES card:
- Background: `--bg-page` for neumorphic; `--bg-surface-raised` (white) for material.
- Radius: 16px (md) — 22px (lg) for hero.
- Padding: 24px.
- Shadow: `--neu-raised` (neumorphic) or `--elev-2` (material).
- Optional 4px-wide eje accent on the left or a colored chip in the corner — never both.

---

## ICONOGRAPHY

### The 4 eje icons

Each of the 4 ejes has a canonical Material Symbols Rounded glyph:

| Eje | Glyph | Color |
|---|---|---|
| Igualdad de género | `add` | Morado |
| Inclusión y no discriminación | `self_improvement` | Azul |
| Cuidados corresponsables | `baby_changing_station` | Amarillo |
| Vida libre de violencias | `volunteer_activism` | Rosa |

If the ONIGIES team has the original line illustrations from `octagono.png` as SVG, drop them into `assets/eje-*.svg` and update the `<EjeIcon>` component in the UI kits to prefer the SVG.

### General UI iconography

For all non-eje icons (chevrons, search, download, filter, menu, etc.) the system uses the **Material Symbols Rounded** font, loaded from Google Fonts CDN:

```html
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0" rel="stylesheet">
```

Rationale: rounded variant matches the friendly neumorphic radii, weight 400 keeps the strokes consistent with our 2px eje-icon line style, and the font ships ~3000 glyphs covering everything an institutional dashboard needs without bespoke artwork.

Usage:

```html
<span class="material-symbols-rounded">download</span>
```

Default size 20px; tap-target wrapper 40px. Icons inherit `color` from their text context — never set fill via SVG attributes.

> Substitution flag: if licensing or offline-bundling requires it, swap Material Symbols Rounded for Phosphor Icons (regular weight) or Lucide (24px, stroke 2). All three were tested for visual fit; Material Symbols Rounded was preferred because it pairs natively with our Material elevations.

### Emoji & unicode

**No emoji in product UI.** No emoji in blog copy either. Unicode characters _are_ used in two specific places:
- `↓` for downloads and `→` for "leer más" links.
- `±` `°` `%` in data labels.

### Logo

- `assets/logo-onigies.svg` — 8-color asterisk. Use at ≥40px height; below that it loses readability and you should use just the wordmark (TBD).
- Lockup variants (mark only, mark + wordmark horizontal, mark + wordmark stacked) are not yet produced in this refresh — flagged in CAVEATS below.

---

## CAVEATS (things to confirm with the ONIGIES team)

1. **Color hexes** — the four eje colors are derived from the original 8-color logo and re-tuned for Material+Neumorphism contrast. Final hexes are open to refinement.
2. **Logo treatment** — the current 8-arm asterisk is kept as-is. With the move to 4 ejes a 4-arm version may make sense; that's a separate design task.
3. **Fonts** — Plus Jakarta Sans & Manrope are Google Fonts substitutions. ONIGIES did not supply licensed fonts.
4. **Eje icons** — we use the Material Symbols glyphs specified by the ONIGIES team (`add`, `self_improvement`, `baby_changing_station`, `volunteer_activism`). If custom line illustrations are produced later they can replace these via `<EjeIcon>`.

---

## SKILL invocation

This repo doubles as an Agent Skill — see `SKILL.md`. To use it in Claude Code or as a downloaded skill, point your agent at this folder and read `README.md` first.
