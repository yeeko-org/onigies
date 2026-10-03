// Stub de `~/store/index.js`: el store real arrastra axios y auto-imports de
// Nuxt; flow.js solo lee `users_by_id`. Módulo sin imports a propósito: el
// factory de vi.mock lo carga mientras flow.js espera ese mismo módulo, y
// cualquier import de vuelta a los stores cerraría el ciclo.
export const mainStoreStub = { users_by_id: {} }

export const useMainStore = () => mainStoreStub
