/* EvidenceTable — list of submitted evidence awaiting review */

const EVIDENCE_DATA = [
  { id: 'EVD-2026-00482', ies: 'BUAP',     eje: 'violeta', subaxis: 'Reglamento de igualdad de género', status: 'review',    submitted: 'Hace 2 h',  reviewer: 'M. Rivas' },
  { id: 'EVD-2026-00481', ies: 'UNAM',     eje: 'rosa',    subaxis: 'Protocolo de atención a violencias',  status: 'approved',  submitted: 'Hace 4 h',  reviewer: 'L. Patiño' },
  { id: 'EVD-2026-00480', ies: 'UAM',      eje: 'azul',    subaxis: 'Política de inclusión LGBTIQ+', status: 'changes', submitted: 'Hace 5 h',  reviewer: 'M. Rivas' },
  { id: 'EVD-2026-00479', ies: 'Cinvestav', eje: 'ambar',  subaxis: 'Lactario y licencias parentales',     status: 'review',    submitted: 'Hace 9 h',  reviewer: 'Sin asignar' },
  { id: 'EVD-2026-00478', ies: 'UASLP',    eje: 'violeta', subaxis: 'Brecha salarial por género',       status: 'approved',  submitted: 'Ayer',      reviewer: 'L. Patiño' },
  { id: 'EVD-2026-00477', ies: 'CIAD',     eje: 'ambar',   subaxis: 'Centro de cuidado infantil',      status: 'rejected',  submitted: 'Ayer',      reviewer: 'A. Cervantes' },
  { id: 'EVD-2026-00476', ies: 'TecNM',    eje: 'azul',    subaxis: 'Plan de accesibilidad universal', status: 'review',    submitted: '2 días',    reviewer: 'M. Rivas' },
  { id: 'EVD-2026-00475', ies: 'BUAP',     eje: 'rosa',    subaxis: 'Comisión de no violencia',          status: 'approved',  submitted: '2 días',    reviewer: 'A. Cervantes' },
];

const EJE_LABEL = {
  violeta: 'Igualdad de género',
  azul:    'Inclusión y no discriminación',
  ambar:   'Cuidados corresponsables',
  rosa:    'Vida libre de violencias',
};

const STATUS_META = {
  approved: { label: 'Aprobada',           cls: 'ok',     icon: 'check' },
  review:   { label: 'En revisión',        cls: 'review', icon: 'schedule' },
  changes:  { label: 'Cambios solicitados',cls: 'warn',   icon: 'edit' },
  rejected: { label: 'Rechazada',          cls: 'rej',    icon: 'close' },
};

const EvidenceTable = ({ selectedId, onSelect }) => (
  <div className="adm-card adm-evidence">
    <div className="adm-card__head">
      <div>
        <div className="adm-card__title">Bandeja de evidencias</div>
        <div className="adm-card__sub">312 evidencias en el ciclo · 84 pendientes</div>
      </div>
      <div className="adm-card__actions">
        <button className="adm-btn adm-btn--ghost">
          <span className="material-symbols-rounded">filter_list</span>
          Filtrar
        </button>
        <button className="adm-btn adm-btn--primary">
          <span className="material-symbols-rounded">upload</span>
          Subir evidencia
        </button>
      </div>
    </div>

    <div className="adm-evidence__grid">
      <div className="adm-evidence__head">Folio</div>
      <div className="adm-evidence__head">Institución</div>
      <div className="adm-evidence__head">Eje · subeje</div>
      <div className="adm-evidence__head">Estado</div>
      <div className="adm-evidence__head">Revisor</div>
      <div className="adm-evidence__head">Recibida</div>
      <div className="adm-evidence__head"></div>

      {EVIDENCE_DATA.map(r => {
        const st = STATUS_META[r.status];
        return (
          <React.Fragment key={r.id}>
            <div className={"adm-evidence__row " + (selectedId === r.id ? "is-selected" : "")}
                 onClick={() => onSelect && onSelect(r.id)}
                 style={{ display: 'contents' }}>
              <div className={"adm-evidence__cell adm-evidence__id " + (selectedId === r.id ? "is-selected" : "")}>{r.id}</div>
              <div className={"adm-evidence__cell adm-evidence__ies " + (selectedId === r.id ? "is-selected" : "")}>{r.ies}</div>
              <div className={"adm-evidence__cell " + (selectedId === r.id ? "is-selected" : "")}>
                <span className={"adm-eje-chip eje-" + r.eje}>
                  <span className="adm-eje-chip__dot"></span>
                  {EJE_LABEL[r.eje]}
                </span>
                <div className="adm-evidence__sub">{r.subaxis}</div>
              </div>
              <div className={"adm-evidence__cell " + (selectedId === r.id ? "is-selected" : "")}>
                <span className={"adm-status adm-status--" + st.cls}>
                  <span className="material-symbols-rounded">{st.icon}</span>
                  {st.label}
                </span>
              </div>
              <div className={"adm-evidence__cell adm-evidence__rev " + (selectedId === r.id ? "is-selected" : "")}>{r.reviewer}</div>
              <div className={"adm-evidence__cell adm-evidence__time " + (selectedId === r.id ? "is-selected" : "")}>{r.submitted}</div>
              <div className={"adm-evidence__cell adm-evidence__chev " + (selectedId === r.id ? "is-selected" : "")}>
                <span className="material-symbols-rounded">chevron_right</span>
              </div>
            </div>
          </React.Fragment>
        );
      })}
    </div>
  </div>
);

window.EvidenceTable = EvidenceTable;
window.EVIDENCE_DATA = EVIDENCE_DATA;
window.EJE_LABEL = EJE_LABEL;
window.STATUS_META = STATUS_META;
