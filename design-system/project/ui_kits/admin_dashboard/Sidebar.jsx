/* Sidebar — deep indigo navigation, fixed left rail */
const Sidebar = ({ active, onSelect }) => {
  const sections = [
    { group: 'Trabajo', items: [
      { key: 'home',       icon: 'dashboard',           label: 'Resumen' },
      { key: 'evidence',   icon: 'description',         label: 'Evidencias', badge: 12 },
      { key: 'reviews',    icon: 'rate_review',         label: 'En revisión' },
      { key: 'audit',      icon: 'fact_check',          label: 'Auditoría' },
    ]},
    { group: 'Datos', items: [
      { key: 'institutions', icon: 'apartment',  label: 'Instituciones' },
      { key: 'instruments',  icon: 'assignment', label: 'Instrumentos' },
      { key: 'index',        icon: 'monitoring', label: 'Índice anual' },
    ]},
    { group: 'Publicación', items: [
      { key: 'publish',    icon: 'public',    label: 'Sitio público' },
      { key: 'reports',    icon: 'article',   label: 'Reportes' },
    ]},
  ];

  return (
    <aside className="adm-sidebar">
      <div className="adm-sidebar__brand">
        <img src="../../assets/logo-onigies.svg" alt="ONIGIES" />
        <div>
          <div className="adm-sidebar__name">ONIGIES</div>
          <div className="adm-sidebar__tag">Admin · 2026</div>
        </div>
      </div>

      <nav className="adm-sidebar__nav">
        {sections.map(s => (
          <div className="adm-sidebar__section" key={s.group}>
            <div className="adm-sidebar__group">{s.group}</div>
            {s.items.map(it => (
              <button
                key={it.key}
                className={"adm-sidebar__link " + (active === it.key ? "is-active" : "")}
                onClick={() => onSelect && onSelect(it.key)}
              >
                <span className="material-symbols-rounded">{it.icon}</span>
                <span className="adm-sidebar__label">{it.label}</span>
                {it.badge ? <span className="adm-sidebar__badge">{it.badge}</span> : null}
              </button>
            ))}
          </div>
        ))}
      </nav>

      <div className="adm-sidebar__foot">
        <div className="adm-sidebar__year">
          <div className="adm-sidebar__year-label">Ciclo activo</div>
          <div className="adm-sidebar__year-value">2026</div>
        </div>
        <button className="adm-sidebar__settings">
          <span className="material-symbols-rounded">settings</span>
        </button>
      </div>
    </aside>
  );
};

window.Sidebar = Sidebar;
