/* EjesGrid — 4-up neumorphic eje KPI cards */

const EJES_DATA = [
  { key: 'violeta', name: 'Igualdad de género',                            short: 'Igualdad',  icon: 'add',                       score: 1.8, delta: +0.1 },
  { key: 'azul',    name: 'Inclusión y no discriminación',                short: 'Inclusión', icon: 'self_improvement',          score: 2.2, delta: +0.3 },
  { key: 'ambar',   name: 'Cuidados corresponsables',                       short: 'Cuidados',  icon: 'baby_changing_station',     score: 1.5, delta: -0.1 },
  { key: 'rosa',    name: 'Una vida libre de discriminaciones y violencias', short: 'Vida libre', icon: 'volunteer_activism',       score: 3.0, delta: +0.4 },
];

const EjeCard = ({ eje, active, onClick }) => (
  <button
    className={"onig-eje eje-" + eje.key + (active ? " is-active" : "")}
    onClick={onClick}
  >
    <div className="onig-eje__ico">
      <span className="material-symbols-rounded">{eje.icon}</span>
    </div>
    <div className="onig-eje__name">{eje.name}</div>
    <div className="onig-eje__score">
      <span className="onig-eje__n">{eje.score.toFixed(1)}</span>
      <span className="onig-eje__of">/ 5</span>
    </div>
    <div className={"onig-eje__delta " + (eje.delta >= 0 ? "up" : "down")}>
      {eje.delta >= 0 ? '+' : '−'}{Math.abs(eje.delta).toFixed(1)} vs año anterior
    </div>
    <div className="onig-eje__subaxes">
      <span>{eje.short}</span>
    </div>
  </button>
);

const EjesGrid = ({ active, onSelect }) => (
  <div className="onig-ejes-grid">
    {EJES_DATA.map(e => (
      <EjeCard key={e.key} eje={e} active={active === e.key}
               onClick={() => onSelect && onSelect(e.key)} />
    ))}
  </div>
);

window.EjeCard = EjeCard;
window.EjesGrid = EjesGrid;
window.EJES_DATA = EJES_DATA;
