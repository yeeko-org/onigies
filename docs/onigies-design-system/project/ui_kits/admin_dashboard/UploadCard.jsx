/* UploadCard — drag-and-drop upload affordance with progress */
const UploadCard = () => (
  <div className="adm-card adm-upload">
    <div className="adm-card__title">Subir nueva evidencia</div>
    <div className="adm-upload__drop">
      <div className="adm-upload__ico">
        <span className="material-symbols-rounded">cloud_upload</span>
      </div>
      <div className="adm-upload__h">Arrastra archivos aquí</div>
      <div className="adm-upload__sub">o haz clic para seleccionar</div>
      <div className="adm-upload__formats">PDF · DOCX · XLSX · PNG · hasta 50 MB</div>
    </div>
    <div className="adm-upload__queue">
      <div className="adm-upload__item">
        <span className="material-symbols-rounded">description</span>
        <div className="adm-upload__item-meta">
          <div className="adm-upload__item-name">protocolo-no-violencia-buap.pdf</div>
          <div className="adm-upload__item-bar">
            <div className="adm-upload__item-fill" style={{width: '68%'}}></div>
          </div>
        </div>
        <div className="adm-upload__item-pct">68%</div>
      </div>
      <div className="adm-upload__item adm-upload__item--done">
        <span className="material-symbols-rounded">check_circle</span>
        <div className="adm-upload__item-meta">
          <div className="adm-upload__item-name">reglamento-igualdad-2026.pdf</div>
          <div className="adm-upload__item-done-meta">Subido · 2.4 MB · listo para revisión</div>
        </div>
      </div>
    </div>
  </div>
);

window.UploadCard = UploadCard;
