from rest_framework import viewsets

from applications.tags.models import Tag
from applications.tags.serializers import TagSerializer
from applications.contacts.mixins import OwnerViewSetMixin


class TagViewSet(OwnerViewSetMixin, viewsets.ModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    related_name = 'tags'
    pagination_class = None
