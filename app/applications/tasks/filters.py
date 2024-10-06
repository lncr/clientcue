from django_filters import rest_framework as filters

from applications.tasks.models import Task
from applications.teams.models import Team, Agent


class TaskFilter(filters.FilterSet):
    team = filters.NumberFilter(field_name='team', method='team_filter')

    class Meta:
        model = Task
        fields = ['team', ]

    def team_filter(self, queryset, name, value):
        team = Team.objects.filter(id=value).first()
        if not team:
            return queryset.none()
        roles = team.roles.all()
        agents = Agent.objects.filter(roles__in=roles)
        queryset = queryset.filter(assigned_to__in=agents)
        return queryset
