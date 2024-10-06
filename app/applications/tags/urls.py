from rest_framework import routers
from applications.tags.views import TagViewSet


router = routers.SimpleRouter()

urlpatterns = []

router.register('tags', TagViewSet)

urlpatterns += router.urls
