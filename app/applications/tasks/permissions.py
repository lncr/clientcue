from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAssignedOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        agents_ids = request.user.agents.all().values_list('id')
        if obj.assigned_to_id in agents_ids:
            return True
        return request.method in SAFE_METHODS
