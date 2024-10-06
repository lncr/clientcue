"""clientcue URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views.generic import TemplateView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from applications.users.social_complete import complete


def trigger_error(request):
    division_by_zero = 1 / 0


schema_view = get_schema_view(
   openapi.Info(
      title="ClientCue API",
      default_version='v1',
      description="Endpoints for ClientCue API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   url='https://clientcue.me/api/v1',
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('api/v1/sentry-debug/', trigger_error),
    path('api/v1/swagger/', schema_view.with_ui(cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/api-auth/', include('rest_framework.urls')),
    path('api/v1/social-auth/complete/<str:backend>/', complete, name='complete'),
    path('api/v1/social-auth/', include('drf_social_oauth2.urls', namespace='drf')),
    path('api/v1/accounts/', include('applications.users.urls')),
    path('api/v1/industries/', include('applications.industries.urls')),
    path('management/', admin.site.urls),
    path('api/v1/company/', include('applications.companies.urls')),
    path('api/v1/', include('applications.contacts.urls')),
    path('api/v1/', include('applications.tags.urls')),
    path('api/v1/', include('applications.teams.urls')),
    path('api/v1/', include('applications.tasks.urls')),
    path('api/v1/', include('applications.chat.urls')),
    # test url for Google Business Account
    path('api/v1/index/', TemplateView.as_view(template_name="email/index.html")),
]
