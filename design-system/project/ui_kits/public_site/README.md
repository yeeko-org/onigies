# Public observatory site — UI kit

The public-facing ONIGIES site. Index gauge, eje breakdowns, historical comparison, per-IES drill-down, downloadable reports.

This is the surface that journalists, students and policy researchers see. It mirrors the layout of the current site (`assets/reference-current-site.png`) but redrawn in the new system: 4 ejes instead of 8, neumorphic KPI tiles, Material-elevated download cards, the signature pastel gradient hero, and tabular-nums for every score.

## Components

- `TopBar.jsx` — sticky top nav: logo, search, ejes menu, blog link
- `Hero.jsx` — pastel gradient hero block with title, year selector
- `IndiceGauge.jsx` — the half-circle gauge (`2.0 de 5`)
- `EjesGrid.jsx` — 4-up neumorphic KPI cards, one per eje
- `HistoricalDots.jsx` — five-year trend (2021–2025)
- `AvanceHistogram.jsx` — distribution bar chart
- `DescargasCard.jsx` — list of report download links
- `IesTable.jsx` — institution-by-institution score matrix
- `Footer.jsx` — institutional footer

Open `index.html` to see them composed.
