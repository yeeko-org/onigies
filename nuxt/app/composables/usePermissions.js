// Fuente única de la lista de permisos de usuario.
// Consumido por StaffUserList (todos), InvitationList y InvitationRow
// (sin `is_active`, ya que en una invitación el usuario aún no existe).

export const USER_PERMISSIONS = [
  {
    key: 'is_active',
    label: 'Activo',
    color: 'grey',
    icon: 'person',
    description: 'La cuenta puede iniciar sesión',
  },
  {
    key: 'reviewer',
    label: 'Revisor/a',
    color: 'blue',
    icon: 'rate_review',
    description: 'Revisa, aprueba y comenta las respuestas de las IES',
  },
  {
    key: 'is_staff',
    label: 'Staff',
    color: 'accent',
    icon: 'shield_person',
    description: 'Acceso al panel administrativo y a la gestión de catálogos',
  },
  {
    key: 'is_superuser',
    label: 'Superuser',
    color: 'primary',
    icon: 'admin_panel_settings',
    description: 'Acceso total, incluyendo gestionar personas usuarias',
  },
]

export const INVITATION_PERMISSIONS = USER_PERMISSIONS.filter(
  p => p.key !== 'is_active'
)
