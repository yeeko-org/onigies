/* HistoricalDots — five-year trend rendered as discs that scale with value */
const HistoricalDots = ({ data }) => {
  const max = Math.max(...data.map(d => d.value));
  return (
    <div className="onig-card onig-history">
      <div className="onig-card__label">Datos históricos</div>
      <div className="onig-history__row">
        {data.map(d => {
          const size = 28 + (d.value / max) * 28;
          return (
            <div className="onig-history__cell" key={d.year}>
              <div className="onig-history__val">{d.value.toFixed(1)}</div>
              <div className="onig-history__disc-wrap">
                <div
                  className="onig-history__disc"
                  style={{ width: size, height: size,
                           background: 'var(--azul-' + (300 + Math.round(d.value * 100)) + ')' }}
                ></div>
              </div>
              <div className="onig-history__year">{d.year}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

window.HistoricalDots = HistoricalDots;
