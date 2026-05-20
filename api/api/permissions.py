from rest_framework.permissions import (
    BasePermission, SAFE_METHODS)

soft_actions = ["POST", "PATCH"]


class IsReviewer(BasePermission):
    """Requires the user to be a reviewer (or admin/staff).
    Restricts access for all methods including GET.
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.is_reviewer


class IsSuperuser(BasePermission):
    """Exige que la persona usuaria sea superusuaria (estricto).

    Para endpoints que gestionan permisos de otras personas o
    invitaciones de staff/revisoras, donde la elevación a staff o
    revisora debe quedar bajo control directo de la superusuaria.
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.is_superuser


class BaseReadOnlyPermission(BasePermission):
    """Base permission that allows read access to everyone"""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_anonymous:
            return False
        return self.has_write_permission(request, view)

    def has_write_permission(self, request, view):
        raise NotImplementedError


class BaseObjectPermission(BaseReadOnlyPermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_anonymous:
            return False
        return self.has_write_permission_object(request, view, obj)

    def has_write_permission_object(self, request, view, obj):
        raise NotImplementedError

    def has_write_permission(self, request, view):
        return True


class BaseHardPermission(BaseObjectPermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if view.action == "add_file":
            return True
        if request.user.is_anonymous:
            return False
        if not request.user.is_reviewer:
            return False
        return self.has_write_permission_object(request, view, obj)


class IsFullEditorOrReadOnly(BaseReadOnlyPermission):
    def has_write_permission(self, request, view):
        return request.user.is_reviewer


class IsAdminOrReadOnly(BaseReadOnlyPermission):
    def has_write_permission(self, request, view):
        return request.user.is_admin


class IsEditorOrCreateOrRead(BaseHardPermission):

    def has_write_permission_object(self, request, view, obj):

        if request.method in soft_actions and obj.status_validation.open_editor:
            return True

        if obj.status_validation.open_editor:
            return request.user.is_reviewer

        return request.user.is_admin


class IsInstitutionOwnerOrSuperuser(BaseObjectPermission):
    """Write access for the user whose institution matches the object's
    institution, or for any superuser. Reads are allowed to any
    authenticated user — per-row visibility must be enforced in
    `get_queryset()` of the consuming ViewSet.

    POST is restricted to superuser (Survey and similar models are
    auto-created by side-effects; manual creation is an admin action).

    Subclasses override `get_institution(obj)` to resolve the owning
    institution for nested models (e.g. `return obj.survey.institution`).
    Returning None denies write.
    """

    def get_institution(self, obj):
        return obj.institution

    def has_write_permission(self, request, view):
        if view.action == 'create':
            return request.user.is_superuser
        # PATCH/PUT/DELETE defer ownership check to object level.
        return True

    def has_write_permission_object(self, request, view, obj):
        user = request.user
        if user.is_superuser:
            return True
        institution = self.get_institution(obj)
        if institution is None:
            return False
        return user.institution_id == institution.pk

