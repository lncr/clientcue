from rest_framework import routers
from applications.contacts.views import ContactViewSet


router = routers.SimpleRouter()

urlpatterns = []

router.register('contacts', ContactViewSet)

urlpatterns += router.urls
