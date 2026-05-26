/* ActivityCard — audit feed of recent actions across the system */
const ActivityCard = () => {
  const items = [
    { who: 'L. Patiño',     verb: 'aprobó',                target: 'EVD-2026-00481',  detail: 'UNAM · Vida libre',       time: '2 min', tone: 'ok' },
    { who: 'BUAP',          verb: 'envió evidencia para',  target: 'Igualdad de género', detail: '4 archivos',          time: '12 min', tone: 'info' },
    { who: 'M. Rivas',      verb: 'solicitó cambios en',   target: 'EVD-2026-00480',  detail: 'UAM · Inclusión',         time: '34 min', tone: 'warn' },
    { who: 'Sistema',       verb: 'recalculó el índice',   target: '2.1 de 5',         detail: '2 IES actualizadas',     time: '2 h',   tone: 'info' },
    { who: 'A. Cervantes',  verb: 'rechazó',               target: 'EVD-2026-00477',  detail: 'CIAD · Cuidados',          time: 'Ayer', tone: 'rej' },
  ];
  return (
    <div className="adm-card adm-activity">
      <div className="adm-card__title">Actividad reciente</div>
      <div className="adm-activity__list">
        {items.map((it, i) => (
          <div className="adm-activity__row" key={i}>
            <div className={"adm-activity__dot adm-activity__dot--" + it.tone}></div>
            <div className="adm-activity__meta">
              <div className="adm-activity__text">
                <b>{it.who}</b> {it.verb} <span className="adm-activity__target">{it.target}</span>
              </div>
              <div className="adm-activity__detail">{it.detail}</div>
            </div>
            <div className="adm-activity__time">{it.time}</div>
          </div>
        ))}
      </div>
      <button className="adm-activity__all">Ver bitácora completa →</button>
    </div>
  );
};

window.ActivityCard = ActivityCard;
