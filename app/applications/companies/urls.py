from django.urls import path, include
from rest_framework.routers import DefaultRouter

from applications.companies.models import Review
from .views import ReviewSet, CompanyViewSet

router = DefaultRouter()
router.register("review", ReviewSet)
router.register("companies", CompanyViewSet)

urlpatterns = [
    path('', include(router.urls))
]
