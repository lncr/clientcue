from rest_framework import routers
from applications.teams.views import (
    TeamModelViewSet,
    AgentModelViewSet,
    RoleModelViewSet,
)


router = routers.SimpleRouter()

urlpatterns = []

router.register('teams', TeamModelViewSet)
router.register('agents', AgentModelViewSet)
router.register('roles', RoleModelViewSet)

urlpatterns += router.urls
