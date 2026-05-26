/* KpiRow — 4 KPIs across the top of the workspace */
const Kpi = ({ label, value, sub, delta, eje, icon }) => (
  <div className={"adm-kpi " + (eje ? "adm-kpi--" + eje : "")}>
    <div className="adm-kpi__row">
      <div className="adm-kpi__ico"><span className="material-symbols-rounded">{icon}</span></div>
      {delta && <div className={"adm-kpi__delta " + (delta.startsWith('+') ? 'up' : 'down')}>{delta}</div>}
    </div>
    <div className="adm-kpi__value">{value}</div>
    <div className="adm-kpi__label">{label}</div>
    {sub && <div className="adm-kpi__sub">{sub}</div>}
  </div>
);

const KpiRow = () => (
  <div className="adm-kpi-row">
    <Kpi
      label="Evidencias pendientes"
      value="84"
      sub="de 312 totales este ciclo"
      delta="+12"
      icon="pending_actions"
      eje="turquesa"
    />
    <Kpi
      label="IES activas en el ciclo"
      value="48"
      sub="36% del total nacional"
      delta="+6"
      icon="apartment"
      eje="turquesa"
    />
    <Kpi
      label="Índice provisional"
      value="2.1"
      sub="recalculado hace 2 h"
      delta="+0.1"
      icon="monitoring"
      eje="turquesa"
    />
    <Kpi
      label="Próxima publicación"
      value="14 d"
      sub="3 de junio · informe 2026"
      icon="event"
      eje="turquesa"
    />
  </div>
);

window.Kpi = Kpi;
window.KpiRow = KpiRow;
