from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from django_filters import rest_framework as filters
from django.conf import settings

from applications.contacts.models import Contact
from applications.contacts.serializers import ContactSerializer, FileActionSerializer
from applications.contacts.filters import ContactsFilterSet
from applications.contacts.utils import from_db_to_excel, from_excel_to_db
from applications.contacts.mixins import OwnerViewSetMixin


class ContactViewSet(OwnerViewSetMixin, viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ContactsFilterSet
    related_name = 'contacts'

    @action(detail=False, methods=['get', ])
    def export_excel(self, request):
        contacts = self.get_queryset()
        filepath = from_db_to_excel(contacts, request.user)
        return Response({'file': settings.MEDIA_URL + filepath})

    @action(detail=False, methods=['post', ], parser_classes=[FormParser, MultiPartParser],
            serializer_class=FileActionSerializer)
    def import_excel(self, request):
        file = request.FILES.get('file')
        path = default_storage.save(f'tmp/{file.name}', ContentFile(file.read()))
        from_excel_to_db(path, request.user)
        return Response({'success': True, })
