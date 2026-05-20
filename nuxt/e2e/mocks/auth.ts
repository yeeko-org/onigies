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
  is_mini_editor: false,
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
  is_mini_editor: false,
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