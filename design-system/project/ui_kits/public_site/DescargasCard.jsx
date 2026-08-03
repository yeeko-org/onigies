/* DescargasCard — list of downloadable report assets */
const DescargasCard = () => {
  const items = [
    { title: 'Resultados principales 2026', sub: 'Resultados por eje y componente', kind: 'PDF · 4.2 MB' },
    { title: 'Desglose de resultados 2026', sub: 'Base de datos con todas las respuestas', kind: 'XLSX · 1.8 MB' },
    { title: 'Informe 2026',                sub: 'Informe anual en formato extenso', kind: 'PDF · 12.6 MB' },
    { title: 'Metodología 2026',            sub: 'Cómo se construye el índice',       kind: 'PDF · 2.1 MB' },
  ];
  return (
    <div className="onig-card onig-descargas">
      <div className="onig-card__label">Descarga de resultados</div>
      <div className="onig-descargas__list">
        {items.map(it => (
          <a className="onig-descargas__item" href="#" key={it.title}>
            <div className="onig-descargas__meta">
              <div className="onig-descargas__title">{it.title}</div>
              <div className="onig-descargas__sub">{it.sub}</div>
              <div className="onig-descargas__kind">{it.kind}</div>
            </div>
            <div className="onig-descargas__btn">
              <span className="material-symbols-rounded">download</span>
            </div>
          </a>
        ))}
      </div>
    </div>
  );
};

window.DescargasCard = DescargasCard;
