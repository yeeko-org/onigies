/* AvanceHistogram — IES distribution by index score (bins of 0.5) */
const AvanceHistogram = ({ bins }) => {
  const max = Math.max(...bins.map(b => b.count));
  return (
    <div className="onig-card onig-histogram">
      <div className="onig-card__label">Avance de las IES</div>
      <div className="onig-histogram__plot">
        <div className="onig-histogram__bars">
          {bins.map((b, i) => {
            const h = (b.count / max) * 100;
            return (
              <div className="onig-histogram__bar-wrap" key={i}>
                <div className="onig-histogram__count">{b.count}</div>
                <div className="onig-histogram__bar"
                     style={{
                       height: h + "%",
                       background: 'var(--azul-' + [200, 300, 400, 500, 500, 600, 600, 700, 700, 800][i] + ')',
                     }}>
                </div>
              </div>
            );
          })}
        </div>
        <div className="onig-histogram__xaxis">
          {bins.map((b, i) => (
            <div key={i}>{b.label}</div>
          ))}
        </div>
      </div>
      <div className="onig-histogram__caption">Avance en el índice de igualdad</div>
    </div>
  );
};

window.AvanceHistogram = AvanceHistogram;
