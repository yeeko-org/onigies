// Fixtures de la sección «Información base» (grupo de flujo `gen`).
// Reflejan `SurveyFullSerializer` con su `general_package` anidado y el
// catálogo Sector tal como viaja en `/catalogs/all/`.
//
// El catálogo real trae 12 poblaciones y 4 autoridades; aquí se reduce a
// las que ejercitan cada bandera (`is_main`, `is_standard_extra`,
// `is_authority`, `is_ies_head`), para que las listas de faltantes de la
// compuerta quepan en una aserción legible.

import { mockRespuestasCatalogs } from './auth'

export const GEN_SURVEY_ID = 100

// Ids de sector, nombrados porque las aserciones del payload los usan.
export const SECTOR_HEAD = 1
export const SECTOR_BOARD = 2
export const SECTOR_ACADEMIC_HEADS = 3
export const SECTOR_UNDERGRADUATE = 10
export const SECTOR_FACULTY = 11
export const SECTOR_EXTERNAL = 20

// Ids de GeneralQuestion: desde task-117 las respuestas escalares viven en
// `question_responses`, así que las aserciones y el contenido completo se
// arman por id, no por columna del Survey.
export const QUESTION_GOVERNMENT = 1
export const QUESTION_ACADEMIC_INSTANCES = 2
export const QUESTION_ADMIN_INSTANCES = 3
export const QUESTION_MEASURES_NON_BINARY = 4
export const QUESTION_MEDIA_PLANS = 5
export const QUESTION_SUPERIOR_PLANS = 6
export const QUESTION_POSTGRADUATE_PLANS = 7

export const mockSectors = [
  {
    id: SECTOR_HEAD, name: 'Titular de la IES', description: '',
    needs_name: false, order: 1, is_main: false, is_authority: true,
    is_standard_extra: false, is_ies_head: true,
  },
  {
    id: SECTOR_BOARD, name: 'Máximo cuerpo colegiado de toda la IES',
    description: '', needs_name: false, order: 2, is_main: false,
    is_authority: true, is_standard_extra: false, is_ies_head: false,
  },
  {
    id: SECTOR_ACADEMIC_HEADS, name: 'Titulares de instancias académicas',
    description: '', needs_name: false, order: 3, is_main: false,
    is_authority: true, is_standard_extra: false, is_ies_head: false,
  },
  {
    id: SECTOR_UNDERGRADUATE, name: 'Alumnado de nivel licenciatura',
    description: '', needs_name: false, order: 10, is_main: true,
    is_authority: false, is_standard_extra: false, is_ies_head: false,
  },
  {
    id: SECTOR_FACULTY, name: 'Personal académico de tiempo completo',
    description: 'Docencia, investigación', needs_name: false, order: 11,
    is_main: true, is_authority: false, is_standard_extra: false,
    is_ies_head: false,
  },
  {
    id: SECTOR_EXTERNAL, name: 'Población externa',
    description: 'Familias, proveedores, etcétera', needs_name: false,
    order: 20, is_main: false, is_authority: false,
    is_standard_extra: true, is_ies_head: false,
  },
]

// El catálogo del dashboard más el de sectores, que es de donde salen los
// renglones de las dos tablas de la sección.
export const mockGenCatalogs = {
  ...mockRespuestasCatalogs,
  sector: mockSectors,
}

// Solo los status del grupo `gen`, con los campos que el motor del front
// consulta: `role` (de quién es el turno), `content_editable` (si el
// contenido se edita en ese status) y `next_statuses` con sus
// `applicable_models`.
export const mockGenFlowStatuses = [
  {
    name: 'gen_draft', public_name: 'Borrador', action_name: null,
    group: 'gen', color: 'blue', icon: 'edit_note', role: 'ies',
    content_editable: true, comment_type: 'none',
    requires_confirmation: false, entry_rules: [],
    next_statuses: ['gen_completed', 'gen_sent'], valid_child_statuses: [],
    applicable_models: [
      ['survey', 'generalgroupresponse'], ['survey', 'generalpackage']],
  },
  {
    name: 'gen_completed', public_name: 'Completado',
    action_name: 'Marcar como completado', group: 'gen', color: 'cyan',
    icon: 'task_alt', role: 'reviewer', content_editable: true,
    comment_type: 'none', requires_confirmation: false, entry_rules: [],
    next_statuses: [], valid_child_statuses: [],
    applicable_models: [['survey', 'generalgroupresponse']],
  },
  {
    name: 'gen_sent', public_name: 'Enviado a revisión',
    action_name: 'Enviar a revisión', group: 'gen', color: 'deep-purple',
    icon: 'send', role: 'reviewer', content_editable: false,
    comment_type: 'optional', requires_confirmation: true,
    confirm_title: '¿Enviar las preguntas generales a revisión?',
    confirm_text: 'Una vez enviadas no podrás modificarlas hasta que la '
      + 'revisión concluya o solicite ajustes.',
    comment_prompt: 'Si gustas, agrega un mensaje para la persona revisora.',
    entry_rules: [], next_statuses: [],
    valid_child_statuses: ['gen_completed'],
    applicable_models: [['survey', 'generalpackage']],
  },
]

const governmentQuestion = {
  id: QUESTION_GOVERNMENT, name: 'is_centralized', q_type: 'boolean', order: 1,
  text: 'Señale cuál de las siguientes descripciones corresponde a la '
    + 'forma de gobierno de su institución.',
  hint: '', label: '', effective_label: '', unit: '',
  addl_config: {
    options: [
      {
        name: 'Descentralizada', value: false,
        description: 'Da autonomía a las autoridades de cada instancia '
          + 'académica y/o administrativa.',
      },
      {
        name: 'Centralizada', value: true,
        description: 'Dota de facultades a su titular para emitir '
          + 'disposiciones vinculantes a todas las áreas académicas y '
          + 'administrativas.',
      },
    ],
  },
}

// `allowNoApply` va al `addl_config` porque es donde el seed lo declara:
// quién ofrece el escape lo manda el catálogo, no el nombre de la pregunta.
const integerQuestion = (
  id: number, name: string, text: string, label: string, order: number,
  allowNoApply = false,
) => ({
  id, name, text, hint: '', label, effective_label: label, unit: label,
  q_type: 'integer', order,
  addl_config: allowNoApply ? { allow_no_apply: true } : {},
})

// Los cinco grupos del instrumento, en el orden que fija `GeneralGroup.order`.
const genGroupCatalogs = [
  {
    name: 'forma_gobierno', public_name: 'Forma de gobierno',
    title: 'Forma de gobierno', subtitle: '', instruction: '',
    is_population: false, order: 1, questions: [governmentQuestion],
  },
  {
    name: 'estructuras', public_name: 'Estructuras', title: 'Estructuras',
    subtitle: '', instruction: '', is_population: false, order: 2,
    questions: [
      integerQuestion(QUESTION_ACADEMIC_INSTANCES, 'academic_instances',
        'Instancias académicas reconocidas en el marco normativo u '
        + 'organigrama de la IES', 'instancias', 1),
      integerQuestion(QUESTION_ADMIN_INSTANCES, 'admin_instances',
        'Instancias administrativas reconocidas en el marco normativo u '
        + 'organigrama de la IES', 'instancias', 2),
    ],
  },
  {
    name: 'poblaciones', public_name: 'Poblaciones', title: 'Poblaciones',
    subtitle: 'Señale las poblaciones que integran a la comunidad de su '
      + 'institución, así como todas aquellas que están presentes física o '
      + 'virtualmente.',
    instruction: 'Para cada población marcada, indique cuántas personas la '
      + 'integran según su sexo y género.',
    is_population: true, order: 3,
    questions: [{
      id: QUESTION_MEASURES_NON_BINARY, name: 'measures_non_binary',
      q_type: 'boolean', order: 1,
      text: 'En sus registros de sexo y género, ¿su institución contempla '
        + 'la categoría no binaria?',
      hint: 'Si responde Sí, las tablas de esta sección incluirán una '
        + 'columna para el conteo de personas no binarias.',
      label: '', effective_label: '', unit: '', addl_config: {},
    }],
  },
  {
    name: 'autoridades', public_name: 'Autoridades', title: 'Autoridades',
    subtitle: '',
    instruction: 'Indique cuántas personas integran, según su sexo y '
      + 'género, cada uno de los siguientes órganos y conjuntos de '
      + 'autoridades de su institución.',
    is_population: true, order: 4, questions: [],
  },
  {
    name: 'planes_estudio', public_name: 'Planes de estudio',
    title: 'Planes de estudio', subtitle: '', instruction: '',
    is_population: false, order: 5,
    questions: [
      integerQuestion(QUESTION_MEDIA_PLANS, 'media_plans',
        'Planes de estudio vigentes de nivel medio superior', 'planes', 1,
        true),
      integerQuestion(QUESTION_SUPERIOR_PLANS, 'superior_plans',
        'Planes de estudio vigentes de nivel superior (licenciatura)',
        'planes', 2, true),
      integerQuestion(QUESTION_POSTGRADUATE_PLANS, 'postgraduate_plans',
        'Planes de estudio vigentes de nivel posgrado (especialidad, '
        + 'maestría y doctorado)', 'planes', 3, true),
    ],
  },
]

// Ids de los GeneralGroupResponse, que son los que viajan en la URL de
// transición del motor de flujo.
export const GEN_GROUP_RESPONSE_IDS: Record<string, number> = {
  forma_gobierno: 301,
  estructuras: 302,
  poblaciones: 303,
  autoridades: 304,
  planes_estudio: 305,
}

const genGroupResponses = genGroupCatalogs.map((catalog) => ({
  id: GEN_GROUP_RESPONSE_IDS[catalog.name],
  survey: GEN_SURVEY_ID,
  general_package: 50,
  general_group: catalog.name,
  general_group_full: catalog,
  status: 'gen_draft',
  status_register: 'pre_start',
  flow_events: [],
  flow_attachments: [],
}))

/**
 * Survey de la IES con la sección en captura: paquete y grupos en
 * borrador (turno de la IES) y el periodo abierto, que es la única
 * combinación en la que los paneles son editables.
 *
 * `overrides` sirve para variar el contenido sin duplicar el andamiaje:
 * los tests de la compuerta cargan un survey ya completo.
 */
export function makeGenSurvey(
  overrides: Record<string, unknown> = {},
): Record<string, unknown> {
  return {
    id: GEN_SURVEY_ID,
    institution: 5,
    period: 2025,
    period_full: {
      year: 2025,
      is_gen_submission_closed: false,
      gen_submission_deadline: '2026-11-01',
      is_bp_submission_closed: false,
      submission_deadline: null,
    },
    measures_non_binary: null,
    sectors: [],
    population_quantities: [],
    question_responses: [],
    general_package: {
      id: 50,
      survey: GEN_SURVEY_ID,
      status: 'gen_draft',
      sent_at: null,
      general_group_responses_count: genGroupResponses.length,
      groups_by_status: { gen_draft: genGroupResponses.length },
      general_group_responses: genGroupResponses,
      flow_events: [],
    },
    ...overrides,
  }
}

const countRow = (
  sector: number, women: number, men: number, present: boolean | null = null,
) => ({
  id: sector, sector, is_present: present, no_apply: false, name: '',
  number_women: women, number_men: men, number_non_binary: null,
})

// Fila de respuesta escalar: el `q_type` decide cuál de las dos columnas
// tipadas carga el dato, la otra queda nula.
const intAnswer = (question: number, value: number) => ({
  general_question: question, no_apply: false,
  value_integer: value, value_boolean: null,
})

const boolAnswer = (question: number, value: boolean) => ({
  general_question: question, no_apply: false,
  value_integer: null, value_boolean: value,
})

/**
 * Contenido que satisface la compuerta de los cinco grupos: las dos
 * poblaciones principales presentes y contadas, la extra presente sin
 * conteo, la titular como un 1 en su conteo, los cuerpos colegiados
 * contados y las preguntas escalares respondidas en sus filas.
 *
 * `measures_non_binary` va en `false` a propósito: con la columna no
 * binaria apagada la compuerta no exige ese tercer conteo. Es la única
 * respuesta que sigue viviendo en una columna del Survey (task-117).
 */
export const completeGenContent = {
  measures_non_binary: false,
  population_quantities: [
    countRow(SECTOR_UNDERGRADUATE, 120, 98, true),
    countRow(SECTOR_FACULTY, 45, 51, true),
    {
      id: SECTOR_EXTERNAL, sector: SECTOR_EXTERNAL, is_present: true,
      no_apply: false, name: '', number_women: null, number_men: null,
      number_non_binary: null,
    },
    countRow(SECTOR_HEAD, 1, 0),
    countRow(SECTOR_BOARD, 14, 11),
    countRow(SECTOR_ACADEMIC_HEADS, 6, 7),
  ],
  question_responses: [
    boolAnswer(QUESTION_GOVERNMENT, false),
    intAnswer(QUESTION_ACADEMIC_INSTANCES, 12),
    intAnswer(QUESTION_ADMIN_INSTANCES, 8),
    // El cero es un dato capturado: la compuerta no lo confunde con vacío.
    intAnswer(QUESTION_MEDIA_PLANS, 0),
    intAnswer(QUESTION_SUPERIOR_PLANS, 15),
    intAnswer(QUESTION_POSTGRADUATE_PLANS, 6),
  ],
}
