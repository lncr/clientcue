from rest_framework import generics

from applications.industries.models import Industry
from applications.industries.serializers import IndustrySerializer


class IndustryListAPIView(generics.ListAPIView):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer
