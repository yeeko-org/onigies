// Fixtures de datos para mocks de auth. Reflejan la forma de respuesta
// del backend (ver api/api/views/login y password-recovery).

export const API_BASE = 'http://localhost:8019/api'

export const mockStaffUser = {
  id: 1,
  email: 'staff@example.com',
  first_name: 'Staff',
  last_name: 'User',
  token: 'test-token-staff-0123456789',
  is_staff: true,
  is_full_editor: true,
  is_ies: false,
  institution: null,
  institution_details: null,
}

export const mockIesUser = {
  id: 2,
  email: 'ies@example.com',
  first_name: 'IES',
  last_name: 'User',
  token: 'test-token-ies-9876543210',
  is_staff: false,
  is_full_editor: false,
  is_ies: true,
  institution: {
    id: 10,
    name: 'Universidad de Ejemplo',
    acronym: 'UE',
  },
  institution_details: {
    id: 10,
    name: 'Universidad de Ejemplo',
    acronym: 'UE',
  },
}

export const mockInvitationUuid = 'inv-uuid-valid-abc123'

export const mockInvitationPayload = {
  uuid: mockInvitationUuid,
  email: 'nuevo@example.com',
  institution_full: {
    id: 20,
    name: 'Institución Nueva',
    acronym: 'IN',
  },
}

export const mockResetToken = 'reset-token-valid-xyz789'

export const mockResetEmail = { email: 'reset@example.com' }

// ── /respuestas (IES) ────────────────────────────────────────────────
// Usuario IES con una encuesta que trae los tres orígenes de estado del
// card: general_package (gen), axis_values (cp) y packages (bp).

export const mockRespuestasCatalogs = {
  axis: [
    { id: 1, short_name: 'Institucional', color: 'indigo',
      icon: 'account_balance' },
    { id: 2, short_name: 'Docencia', color: 'teal', icon: 'school' },
  ],
  collections: [],
  filter_groups: [],
  levels: [],
  status_control: [],
}

export const mockRespuestasFlowStatuses = [
  { name: 'gen_draft', public_name: 'Datos base — borrador',
    color: 'blue-grey', icon: 'edit' },
  { name: 'cp_draft', public_name: 'En captura',
    color: 'orange', icon: 'edit_note' },
  { name: 'bp_draft', public_name: 'Buenas prácticas — borrador',
    color: 'pink', icon: 'lightbulb' },
]

export const mockIesRespuestasUser = {
  id: 10,
  email: 'ies-respuestas@example.com',
  first_name: 'IES',
  last_name: 'Respuestas',
  token: 'test-token-ies-respuestas',
  is_staff: false,
  is_full_editor: false,
  is_ies: true,
  institution: {
    id: 5,
    name: 'Universidad de Prueba',
    acronym: 'UP',
    is_public: true,
    logo: null,
  },
  institution_details: {
    surveys: [
      {
        id: 100,
        period: 2025,
        general_package: { status: 'gen_draft' },
        axis_values: [
          { id: 201, axis: 1, status: 'cp_draft' },
          { id: 202, axis: 2, status: 'cp_draft' },
        ],
        packages: [{ status: 'bp_draft' }],
      },
    ],
  },
}