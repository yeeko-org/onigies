/* TopBar — sticky public-site navigation */
const TopBar = () => {
  const [showEjes, setShowEjes] = React.useState(false);
  const ejes = [
    { key: 'violeta', name: 'Igualdad de género',                            icon: 'add' },
    { key: 'azul',    name: 'Inclusión y no discriminación',                icon: 'self_improvement' },
    { key: 'ambar',   name: 'Cuidados corresponsables',                       icon: 'baby_changing_station' },
    { key: 'rosa',    name: 'Una vida libre de discriminaciones y violencias', icon: 'volunteer_activism' },
  ];
  return (
    <header className="onig-topbar">
      <a className="onig-topbar__brand" href="#">
        <img src="../../assets/logo-onigies.svg" alt="ONIGIES" />
        <span>ONIGIES</span>
      </a>

      <div className="onig-topbar__search">
        <span className="material-symbols-rounded">search</span>
        <input placeholder="Buscar institución" />
      </div>

      <nav className="onig-topbar__nav">
        <button
          className={"onig-topbar__navlink " + (showEjes ? "is-open" : "")}
          onClick={() => setShowEjes(v => !v)}
        >
          Ejes
          <span className="material-symbols-rounded">expand_more</span>
        </button>
        <a className="onig-topbar__navlink" href="#">Metodología</a>
        <a className="onig-topbar__navlink" href="#">Blog</a>
        <button className="onig-topbar__cta">Reporte 2026 ↓</button>

        {showEjes && (
          <div className="onig-topbar__menu" onMouseLeave={() => setShowEjes(false)}>
            {ejes.map(e => (
              <a key={e.key} className={"onig-topbar__menuitem eje-" + e.key} href="#">
                <span className="material-symbols-rounded">{e.icon}</span>
                <span>{e.name}</span>
                <span className="material-symbols-rounded onig-topbar__chev">arrow_forward</span>
              </a>
            ))}
          </div>
        )}
      </nav>
    </header>
  );
};

window.TopBar = TopBar;
