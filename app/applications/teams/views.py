from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from applications.teams.models import Agent, Role, Team
from applications.teams.serializers import (
    AgentSerializer,
    RoleSerializer,
    TeamSerializer,
)
from applications.contacts.mixins import OwnerViewSetMixin


class RoleModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Role.objects.all().select_related('team')
    serializer_class = RoleSerializer
    filter_fields = ['team', ]

    def get_queryset(self):
        user = self.request.user
        qs = self.queryset.filter(team__owner_id=user.id)
        agents = user.agents.prefetch_related('roles')

        for agent in agents:
            for role in agent.roles.all():
                team = role.team
                qs = qs | team.roles.all()

        return qs.distinct().order_by('-id')


class AgentModelViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated, ]
    queryset = Agent.objects.all().prefetch_related('roles')
    serializer_class = AgentSerializer

    def get_queryset(self):
        user = self.request.user
        owned_team_ids = user.teams.values_list('id')
        user_agents = user.agents.all()
        user_roles = Role.objects.filter(agents__in=user_agents)
        team_ids = list(owned_team_ids)

        for role in user_roles:
            team_ids.append(role.team.id)

        roles_of_teams = Role.objects.filter(team__in=team_ids)
        return self.queryset.filter(roles__in=roles_of_teams).order_by('-id')


class TeamModelViewSet(OwnerViewSetMixin, viewsets.ModelViewSet):

    queryset = Team.objects.all().order_by('-id')
    serializer_class = TeamSerializer
    related_name = 'teams'

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        for agent in user.agents.all().prefetch_related('roles'):
            qs = qs | Team.objects.filter(roles__in=agent.roles.all())
        return qs.distinct().order_by('-id')
