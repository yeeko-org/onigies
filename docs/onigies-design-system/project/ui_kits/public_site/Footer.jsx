/* Footer — institutional links + credits */
const Footer = () => (
  <footer className="onig-footer">
    <div className="onig-footer__top">
      <div className="onig-footer__brand">
        <img src="../../assets/logo-onigies.svg" alt="" />
        <div>
          <div className="onig-footer__name">ONIGIES</div>
          <div className="onig-footer__tag">Observatorio Nacional para la Igualdad de Género en las IES</div>
        </div>
      </div>
      <div className="onig-footer__cols">
        <div>
          <div className="onig-footer__h">Observatorio</div>
          <a href="#">Quiénes somos</a>
          <a href="#">Metodología</a>
          <a href="#">Equipo</a>
          <a href="#">Contacto</a>
        </div>
        <div>
          <div className="onig-footer__h">Ejes</div>
          <a href="#">Igualdad de género</a>
          <a href="#">Inclusión y no discriminación</a>
          <a href="#">Cuidados corresponsables</a>
          <a href="#">Vida libre de discriminaciones y violencias</a>
        </div>
        <div>
          <div className="onig-footer__h">Publicaciones</div>
          <a href="#">Informe 2026</a>
          <a href="#">Reportes anteriores</a>
          <a href="#">Notas metodológicas</a>
          <a href="#">Blog</a>
        </div>
      </div>
    </div>
    <div className="onig-footer__bot">
      <div>© 2026 ONIGIES — Observatorio Nacional para la Igualdad de Género en las IES.</div>
      <div>Datos liberados bajo licencia abierta. Última actualización: 26 mayo 2026.</div>
    </div>
  </footer>
);

window.Footer = Footer;
