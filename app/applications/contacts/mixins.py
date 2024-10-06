from rest_framework.permissions import IsAuthenticated, IsAdminUser

from applications.contacts.permissions import IsOwner


class OwnerViewSetMixin:

    permission_classes = [IsAuthenticated, IsAdminUser | IsOwner]

    def perform_create(self, serializer):
        owner = self.request.user
        return serializer.save(owner=owner)

    def get_queryset(self):
        if self.request.user.is_admin:
            return self.queryset.order_by('-id')
        else:
            owner = self.request.user
            related_model_manager = getattr(owner, self.related_name)
            return related_model_manager.all().order_by('-id')
