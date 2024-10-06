from django.urls import path

from applications.industries.views import IndustryListAPIView

app_name = 'industries'

urlpatterns = [
    path('', IndustryListAPIView.as_view(), name='industry-list'),
]
