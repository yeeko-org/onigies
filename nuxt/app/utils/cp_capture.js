/**
 * Lógica pura de la captura del cuestionario principal (flujo `cp`): el
 * borrador editable de cada grupo, el payload del PATCH y los resúmenes
 * por status. Sin Vue ni stores, para poder probarla aislada.
 *
 * El borrador de un grupo es un objeto por id de pregunta; el payload
 * solo lleva las filas que cambiaron contra la línea base, porque el
 * backend hace upsert por pregunta y nunca borra por omisión: mandar una
 * fila intacta crearía respuestas vacías donde la IES no tocó nada.
 */

// Por tipo de pregunta: la lista de preguntas en `observable_full`, la
// lista de respuestas en el grupo y cómo se arma cada fila del borrador.
export const CP_TYPES = {
  a_questions: {
    questions: 'a_questions',
    responses: 'a_responses',
    empty: () => ({ selected_option: null }),
    fromResponse: (r) => ({ selected_option: r.selected_option ?? null }),
  },
  b_questions: {
    questions: 'b_questions',
    responses: 'b_responses',
    empty: () => ({
      academic_instances_complying: null,
      admin_instances_complying: null,
    }),
    fromResponse: (r) => ({
      academic_instances_complying: r.academic_instances_complying ?? null,
      admin_instances_complying: r.admin_instances_complying ?? null,
    }),
  },
  reach: {
    questions: 'reach_questions',
    responses: 'reach_responses',
    empty: () => ({ not_focalized: false, sectors: [] }),
    fromResponse: (r) => ({
      not_focalized: !!r.not_focalized,
      sectors: [...(r.sectors || [])].sort((a, b) => a - b),
    }),
  },
  plans: {
    questions: 'plan_questions',
    responses: 'plan_responses',
    empty: () => ({
      media_plans: null, superior_plans: null, postgraduate_plans: null,
    }),
    fromResponse: (r) => ({
      media_plans: r.media_plans ?? null,
      superior_plans: r.superior_plans ?? null,
      postgraduate_plans: r.postgraduate_plans ?? null,
    }),
  },
  special: {
    questions: 'special_questions',
    responses: 'special_responses',
    empty: () => ({ total: null, complying: null }),
    fromResponse: (r) => ({
      total: r.total ?? null,
      complying: r.complying ?? null,
    }),
  },
}

// Niveles de planes de estudio en el orden del instrumento; `field` es a
// la vez la columna de PlanResponse y la pregunta general que la acota.
export const PLAN_LEVELS = [
  { field: 'media_plans', label: 'Nivel medio superior' },
  { field: 'superior_plans', label: 'Licenciatura' },
  { field: 'postgraduate_plans', label: 'Posgrado' },
]

export function questionsOf(observable, typeName) {
  const spec = CP_TYPES[typeName]
  return spec ? (observable?.[spec.questions] || []) : []
}

/** Borrador del grupo: una fila por pregunta del observable. */
export function buildDraft(group, observable) {
  const spec = CP_TYPES[group?.question_type]
  if (!spec) return {}
  const byQuestion = {}
  for (const r of group[spec.responses] || [])
    byQuestion[r.question] = r
  const draft = {}
  for (const q of questionsOf(observable, group.question_type)) {
    const saved = byQuestion[q.id]
    draft[q.id] = saved ? spec.fromResponse(saved) : spec.empty()
  }
  return draft
}

function normalizeRow(row) {
  if (!row || !Array.isArray(row.sectors)) return row
  return { ...row, sectors: [...row.sectors].sort((a, b) => a - b) }
}

const sameRow = (a, b) =>
  JSON.stringify(normalizeRow(a)) === JSON.stringify(normalizeRow(b))

/** Ids de pregunta cuya fila difiere de la línea base. */
export function changedQuestions(draft, baseline) {
  return Object.keys(draft || {})
    .filter((qid) => !sameRow(draft[qid], baseline?.[qid]))
}

/** `{<lista del tipo>: [filas cambiadas]}`, o null si no hay cambios. */
export function buildGroupPayload(typeName, draft, baseline) {
  const spec = CP_TYPES[typeName]
  if (!spec) return null
  const rows = changedQuestions(draft, baseline).map((qid) => ({
    question: Number(qid),
    ...normalizeRow(draft[qid]),
  }))
  return rows.length ? { [spec.responses]: rows } : null
}

/** Conteo `{status: n}` de una lista de objetos del flujo. */
export function countByStatus(rows) {
  const counts = {}
  for (const row of rows || [])
    if (row?.status) counts[row.status] = (counts[row.status] || 0) + 1
  return counts
}

/**
 * ¿Le queda trabajo de captura a la IES en este status? Por regla del
 * catálogo, no por nombre: es su turno y el contenido es editable. Lo
 * demás (en manos de la revisión, pospuesto, aprobado, terminal) cuenta
 * como resuelto de su lado.
 */
export function isPendingForIes(status) {
  return !!status && status.role === 'ies' && !!status.content_editable
}

/**
 * Cuántos observables de un conteo `{status: n}` ya no esperan captura
 * de la IES. `getStatus` resuelve el nombre contra el catálogo.
 */
export function resolvedCount(byStatus, getStatus) {
  let resolved = 0
  let total = 0
  for (const [name, n] of Object.entries(byStatus || {})) {
    total += n
    if (!isPendingForIes(getStatus(name))) resolved += n
  }
  return { resolved, total }
}

/**
 * Copia sobre el observable en pantalla el estado que devolvió el
 * servidor (respuesta inicial, status y timeline, propios y de cada
 * grupo). Las respuestas de los grupos no se tocan: ahí vive la línea
 * base del borrador que la IES puede tener a medias.
 */
export function applyObservableState(target, data) {
  if (!target || !data) return
  target.value = data.value
  target.status = data.status
  target.flow_events = data.flow_events
  const fresh = Object.fromEntries(
    (data.group_responses || []).map((g) => [g.id, g]))
  for (const group of target.group_responses || []) {
    const g = fresh[group.id]
    if (!g) continue
    group.status = g.status
    group.flow_events = g.flow_events
  }
}

/**
 * `{status: n}` convertido en filas `{name, count, st}` resueltas contra
 * el catálogo, la más urgente primero (priority del status).
 */
export function statusRows(byStatus, getStatus) {
  return Object.entries(byStatus || {})
    .map(([name, count]) => ({ name, count, st: getStatus(name) }))
    .filter((row) => row.st)
    .sort((a, b) => (b.st.priority || 0) - (a.st.priority || 0))
}

/**
 * La cola de un rol en un eje: cuántos observables y cuántos grupos
 * esperan su transición (el `role` del status es de quién es el turno).
 */
export function countInTurn(axis, role, getStatus) {
  let observables = 0
  let groups = 0
  for (const obs of axis?.observable_responses || []) {
    if (getStatus(obs.status)?.role === role) observables += 1
    for (const g of obs.group_responses || [])
      if (getStatus(g.status)?.role === role) groups += 1
  }
  return { observables, groups }
}

/**
 * El grupo que pide atención de un rol dentro de un observable: el de
 * mayor prioridad entre los que están en su turno y superan la prioridad
 * del propio observable (p. ej. uno devuelto con ajustes, o uno que la
 * IES completó mientras el observable sigue en llenado).
 */
export function attentionGroup(observable, role, getStatus) {
  const own = getStatus(observable?.status)?.priority || 0
  let best = null
  let bestPriority = own
  for (const g of observable?.group_responses || []) {
    const st = getStatus(g.status)
    if (st?.role !== role || (st.priority || 0) <= bestPriority) continue
    best = g
    bestPriority = st.priority || 0
  }
  return best
}
