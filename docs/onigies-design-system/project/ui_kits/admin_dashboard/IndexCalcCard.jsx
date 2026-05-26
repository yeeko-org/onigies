/* IndexCalcCard — status of the current index calculation */
const IndexCalcCard = () => {
  const ejes = [
    { key: 'violeta', name: 'Igualdad de género',             pct: 76 },
    { key: 'azul',    name: 'Inclusión y no discriminación', pct: 88 },
    { key: 'ambar',   name: 'Cuidados corresponsables',        pct: 64 },
    { key: 'rosa',    name: 'Vida libre de violencias',         pct: 92 },
  ];
  return (
    <div className="adm-card adm-calc">
      <div className="adm-calc__row">
        <div>
          <div className="adm-card__title">Cálculo del índice 2026</div>
          <div className="adm-card__sub">Última actualización: hace 2 h</div>
        </div>
        <div className="adm-calc__big">
          <div className="adm-calc__big-value">2.1</div>
          <div className="adm-calc__big-of">provisional</div>
        </div>
      </div>

      <div className="adm-calc__bars">
        {ejes.map(e => (
          <div className="adm-calc__bar-row" key={e.key}>
            <div className="adm-calc__bar-label">
              <span className={"adm-eje-chip__dot eje-dot-" + e.key}></span>
              {e.name}
            </div>
            <div className="adm-calc__bar-track">
              <div className={"adm-calc__bar-fill eje-bar-" + e.key}
                   style={{width: e.pct + '%'}}></div>
            </div>
            <div className="adm-calc__bar-pct">{e.pct}%</div>
          </div>
        ))}
      </div>

      <div className="adm-calc__actions">
        <button className="adm-btn adm-btn--ghost">
          <span className="material-symbols-rounded">refresh</span>
          Recalcular
        </button>
        <button className="adm-btn adm-btn--primary">
          Cerrar ciclo y publicar →
        </button>
      </div>
    </div>
  );
};

window.IndexCalcCard = IndexCalcCard;
