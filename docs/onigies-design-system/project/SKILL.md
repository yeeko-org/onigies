---
name: onigies-design
description: Use this skill to generate well-branded interfaces and assets for ONIGIES (Observatorio Nacional para la Igualdad de Género en las Instituciones de Educación Superior), either for production or throwaway prototypes/mocks/etc. Contains essential design guidelines, colors, type, fonts, assets, and UI kit components for prototyping the public observatory site and the internal admin dashboard.
user-invocable: true
---

Read the `README.md` file within this skill, and explore the other available files.

If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view. If working on production code, you can copy assets and read the rules here to become an expert in designing with this brand.

If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.

## Quick facts about ONIGIES

- Mexican observatory that publishes an annual gender-equality index for IES (Instituciones de Educación Superior).
- Index is now organized in **4 ejes** (reduced from 8): Igualdad de género (morado), Inclusión y no discriminación (azul), Cuidados corresponsables (amarillo), Una vida libre de discriminaciones y violencias (rosa).
- A **5th brand color** — **turquesa** `#14A8A0` — is the primary action color, used across both surfaces for CTAs, links, the Índice Global gauge and KPI, etc. It sits outside the 4-eje palette so it never reads as a data tag.
- Two surfaces: a **public observatory site** (data-forward, informational) and an **admin dashboard** (internal, indigo chrome with turquesa accents).
- Visual system is **Material Design + soft Neumorphism** on a warm off-white canvas (`#F6F4F9`).
- Voice is **institutional but warm** — Spanish (México), sentence case, no emoji, second-person imperative for UI labels.

## Files of interest

- `colors_and_type.css` — all tokens. Import this first when building anything new.
- `README.md` — full system documentation (palette, type, motion, iconography, content fundamentals, visual foundations).
- `assets/` — logo, octagon wheel, reference screenshots.
- `ui_kits/public_site/` — JSX components + index.html for the public observatory.
- `ui_kits/admin_dashboard/` — JSX components + index.html for the internal admin.
- `preview/` — design-system tab cards (palette, type, components).

## Build rules

- Never put a neumorphic card on pure white — use `--bg-page`.
- Use brand color as an **accent**, not as a background, unless it's a hero promo card.
- **Turquesa is primary** across both surfaces — CTAs, links, the Índice Global gauge & big KPI, focus rings. The 4 eje colors (morado / azul / amarillo / rosa) are reserved for eje-tagged data only.
- For the admin dashboard, the chrome is `--indigo-700` and the primary affordance is `--primary-500` (turquesa). The 4 eje colors appear only as data tags.
- Tabular numerals on every number in a column.
- Material elevation for floating UI (menus, dialogs); Neumorphism for stationary UI (KPI tiles, score discs, inputs).
- No emoji. Use Material Symbols Rounded for all non-eje iconography.
