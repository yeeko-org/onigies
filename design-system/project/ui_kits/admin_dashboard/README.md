# Admin dashboard — UI kit

Internal app used by ONIGIES staff and IES representatives to upload evidence, manage instrument responses, audit submissions, and publish the annual index.

## Distinction from the public site

The admin uses the **same brand tokens** as the public site but anchors its chrome in a deeper, calmer palette so long working sessions don't fatigue the eye:

- Sidebar: `--indigo-700` (`#2C2F6E`) with white text
- Primary affordance: `--turquesa-500` (`#14A8A0`)
- The 4 brand colors (rosa / violeta / azul / ámbar) still appear, but only as **data tags** — eje chips on evidence cards, score-bar fills, KPI accents.
- Page background: `--bg-page` (the neumorphic canvas), same as the public site.

## Components

- `Sidebar.jsx` — collapsible nav, deep indigo
- `AdminTopBar.jsx` — workspace switcher, search, notifications, user
- `KpiRow.jsx` — 4 admin KPIs across the top of the workspace
- `EvidenceTable.jsx` — list of evidence submissions awaiting review
- `EvidenceDetail.jsx` — right-side drawer showing the selected submission
- `UploadCard.jsx` — upload affordance (drag-and-drop card)
- `ActivityCard.jsx` — recent activity / audit feed
- `IndexCalcCard.jsx` — current index calculation status

Open `index.html` to see them composed.
