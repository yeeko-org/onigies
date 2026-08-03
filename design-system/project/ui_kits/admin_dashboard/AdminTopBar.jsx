/* AdminTopBar — workspace selector, search, notifications, profile */
const AdminTopBar = () => (
  <header className="adm-topbar">
    <div className="adm-topbar__crumb">
      <span className="adm-topbar__crumb-eye">RESUMEN</span>
      <span className="material-symbols-rounded">chevron_right</span>
      <span>Bandeja de evidencias</span>
    </div>

    <div className="adm-topbar__search">
      <span className="material-symbols-rounded">search</span>
      <input placeholder="Buscar evidencia, institución, eje…" />
      <span className="adm-topbar__shortcut">⌘ K</span>
    </div>

    <div className="adm-topbar__actions">
      <button className="adm-topbar__iconbtn" title="Filtros">
        <span className="material-symbols-rounded">tune</span>
      </button>
      <button className="adm-topbar__iconbtn has-dot" title="Notificaciones">
        <span className="material-symbols-rounded">notifications</span>
      </button>
      <div className="adm-topbar__user">
        <div className="adm-topbar__avatar">MR</div>
        <div className="adm-topbar__user-meta">
          <div className="adm-topbar__user-name">Mariana Rivas</div>
          <div className="adm-topbar__user-role">Coordinadora · ONIGIES</div>
        </div>
        <span className="material-symbols-rounded">expand_more</span>
      </div>
    </div>
  </header>
);

window.AdminTopBar = AdminTopBar;
