// Documentos públicos de la API (`/public-documents/`): su descarga no pide
// token, así que basta un enlace directo, sin pasar por `$api`.

// El Word del cuestionario, sembrado en el backend con este slug fijo.
export const DOCX_SLUG = 'cuestionario-2026'

export function docxUrl(apiUrl) {
  return `${apiUrl}/public-documents/${DOCX_SLUG}/download/`
}
