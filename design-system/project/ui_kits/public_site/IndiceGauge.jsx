/* IndiceGauge — half-circle gauge showing 0..5 with needle */
const IndiceGauge = ({ value = 2.0 }) => {
  const clamped = Math.max(0, Math.min(5, value));
  // Arc geometry: 200x110 viewbox, half-circle from -90deg to +90deg
  const cx = 110, cy = 100, r = 84;
  const startAngle = Math.PI;             // 180°
  const endAngle = 2 * Math.PI;           // 360° (0°)
  const angleFor = v => startAngle + (v / 5) * (endAngle - startAngle);
  const polar = (a, rad = r) => [cx + rad * Math.cos(a), cy + rad * Math.sin(a)];

  // 5 segments, each a stroke arc
  const segs = [0, 1, 2, 3, 4].map(i => {
    const a1 = angleFor(i), a2 = angleFor(i + 1);
    const [x1, y1] = polar(a1), [x2, y2] = polar(a2);
    const large = 0;
    return {
      d: `M ${x1} ${y1} A ${r} ${r} 0 ${large} 1 ${x2} ${y2}`,
      shade: `var(--turquesa-${[100, 100, 500, 700, 900][i]})`,
    };
  });

  const needleA = angleFor(clamped);
  const [nx, ny] = polar(needleA, r + 4);
  const [bx, by] = polar(needleA + Math.PI, 6);

  return (
    <div className="onig-gauge">
      <div className="onig-card__label">Índice de Igualdad de Género IES México</div>
      <svg viewBox="0 0 220 130" className="onig-gauge__svg">
        {segs.map((s, i) => (
          <path key={i} d={s.d} stroke={s.shade} strokeWidth="18"
                fill="none" strokeLinecap="butt" />
        ))}
        {[0,1,2,3,4,5].map(t => {
          const a = angleFor(t);
          const [tx, ty] = polar(a, r + 22);
          return (
            <text key={t} x={tx} y={ty} fontSize="11"
                  textAnchor="middle" dominantBaseline="middle"
                  fontFamily="Manrope" fontWeight="600" fill="var(--fg-3)">{t}</text>
          );
        })}
        {/* needle */}
        <line x1={bx} y1={by} x2={nx} y2={ny}
              stroke="var(--neutral-900)" strokeWidth="3.5" strokeLinecap="round" />
        <circle cx={cx} cy={cy} r="6" fill="var(--neutral-900)" />
      </svg>
      <div className="onig-gauge__readout">
        <span className="onig-gauge__value">{clamped.toFixed(1)}</span>
        <span className="onig-gauge__of">de 5</span>
      </div>
    </div>
  );
};

window.IndiceGauge = IndiceGauge;
