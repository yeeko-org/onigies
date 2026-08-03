/* Hero — gradient pastel wash with title + year selector */
const Hero = ({ year, onYearChange }) => {
  const years = [2021, 2022, 2023, 2024, 2025, 2026];
  const [open, setOpen] = React.useState(false);
  return (
    <section className="onig-hero">
      <div className="onig-hero__bg"></div>
      <div className="onig-hero__grain"></div>
      <div className="onig-hero__inner">
        <div>
          <div className="onig-hero__eye">Resultados {year}</div>
          <h1 className="onig-hero__title">
            Observatorio Nacional para la Igualdad de Género <br/>
            en las Instituciones de Educación Superior
          </h1>
          <p className="onig-hero__sub">
            48 instituciones medidas en 4 ejes. Un índice anual,
            verificado y de acceso público.
          </p>
        </div>
        <div className="onig-hero__yearpicker">
          <div className="onig-hero__yearpicker__label">Año mostrado</div>
          <button
            className="onig-hero__yearpicker__btn"
            onClick={() => setOpen(o => !o)}
          >
            <span>{year}</span>
            <span className="material-symbols-rounded">expand_more</span>
          </button>
          {open && (
            <div className="onig-hero__yearpicker__menu" onMouseLeave={() => setOpen(false)}>
              {years.map(y => (
                <button
                  key={y}
                  className={"onig-hero__yearpicker__item " + (y === year ? "is-active" : "")}
                  onClick={() => { onYearChange(y); setOpen(false); }}
                >{y}</button>
              ))}
            </div>
          )}
        </div>
      </div>
    </section>
  );
};

window.Hero = Hero;
