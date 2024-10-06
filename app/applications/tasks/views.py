from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters

from applications.tasks.filters import TaskFilter
from applications.tasks.models import Task
from applications.tasks.serializers import TaskSerializer
from applications.tasks.permissions import IsAssignedOrReadOnly


class TaskModelViewSet(ModelViewSet):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated, IsAssignedOrReadOnly | IsAdminUser, )
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = TaskFilter
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return self.queryset
        team = self.request.query_params.get('team')
        if team is None:
            self.queryset = self.queryset.none()
        return self.queryset

    @action(methods=['get', ], detail=False)
    def assigned(self, request):
        user = request.user
        agents = user.agents.all()
        qs = self.queryset.filter(assigned_to__in=agents)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
