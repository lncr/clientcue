from rest_framework.routers import SimpleRouter
from applications.tasks.views import TaskModelViewSet


router = SimpleRouter()

router.register('tasks', TaskModelViewSet)
urlpatterns = []

urlpatterns += router.urls
