from .models import Review, Company
from .serializers import ReviewSerializer, CompanySerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from rest_framework import viewsets
from .serializers import CompanySerializer
from rest_framework import mixins

class ReviewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    

class CompanyViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin, 
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin, 
                    GenericViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
