/* IesTable — per-institution score matrix.
   Rows: institutions. Columns: índice + the 4 ejes. */

const IES_DATA = [
  { code: 'TODAS', name: 'Todas las IES', total: 2.0, rosa: 3.0, violeta: 1.8, azul: 2.2, ambar: 1.5 },
  { code: 'BUAP',   name: 'BUAP',   total: 2.6, rosa: 3.4, violeta: 2.2, azul: 2.5, ambar: 2.1 },
  { code: 'CIAD',   name: 'CIAD',   total: 1.5, rosa: 1.7, violeta: 1.1, azul: 2.4, ambar: 0.9 },
  { code: 'CINVST', name: 'Cinvestav', total: 2.3, rosa: 2.8, violeta: 2.6, azul: 2.4, ambar: 1.6 },
  { code: 'UAM',    name: 'UAM',    total: 2.9, rosa: 3.1, violeta: 2.8, azul: 3.4, ambar: 2.3 },
  { code: 'UNAM',   name: 'UNAM',   total: 3.4, rosa: 3.8, violeta: 3.2, azul: 3.6, ambar: 3.0 },
  { code: 'UASLP',  name: 'UASLP',  total: 1.9, rosa: 2.4, violeta: 1.4, azul: 2.1, ambar: 1.7 },
  { code: 'ITESM',  name: 'TecNM',  total: 1.4, rosa: 1.6, violeta: 1.2, azul: 1.8, ambar: 1.0 },
];

const ScoreCell = ({ value, eje }) => {
  // 0..5 → bar width 6%..100%
  const pct = 6 + (value / 5) * 94;
  return (
    <div className="onig-iestable__cell">
      <div className="onig-iestable__bar-bg">
        <div
          className={"onig-iestable__bar eje-bar-" + eje}
          style={{ width: pct + '%' }}
        ></div>
      </div>
      <span className="onig-iestable__val">{value.toFixed(1)}</span>
    </div>
  );
};

const IesTable = ({ filter, onFilter }) => {
  const rows = filter
    ? IES_DATA.filter(r => r.name.toLowerCase().includes(filter.toLowerCase()))
    : IES_DATA;

  return (
    <div className="onig-card onig-iestable">
      <div className="onig-iestable__head">
        <div>
          <div className="onig-card__label">Resultados de las 48 IES</div>
          <div className="onig-iestable__hint">Ordena por columna o filtra por institución</div>
        </div>
        <div className="onig-iestable__filter">
          <span className="material-symbols-rounded">search</span>
          <input
            placeholder="Filtrar IES…"
            value={filter || ''}
            onChange={e => onFilter && onFilter(e.target.value)}
          />
        </div>
      </div>

      <div className="onig-iestable__grid">
        <div className="onig-iestable__col-head">Institución</div>
        <div className="onig-iestable__col-head">Índice global</div>
        <div className="onig-iestable__col-head"><span className="dot eje-dot-violeta"></span>Igualdad</div>
        <div className="onig-iestable__col-head"><span className="dot eje-dot-azul"></span>Inclusión</div>
        <div className="onig-iestable__col-head"><span className="dot eje-dot-ambar"></span>Cuidados</div>
        <div className="onig-iestable__col-head"><span className="dot eje-dot-rosa"></span>Vida libre</div>

        {rows.map(r => (
          <React.Fragment key={r.code}>
            <div className={"onig-iestable__name " + (r.code === 'TODAS' ? 'is-aggregate' : '')}>
              {r.name}
            </div>
            <ScoreCell value={r.total}   eje="primary" />
            <ScoreCell value={r.violeta} eje="violeta" />
            <ScoreCell value={r.azul}    eje="azul" />
            <ScoreCell value={r.ambar}   eje="ambar" />
            <ScoreCell value={r.rosa}    eje="rosa" />
          </React.Fragment>
        ))}
      </div>
    </div>
  );
};

window.IesTable = IesTable;
window.IES_DATA = IES_DATA;
