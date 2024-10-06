from rest_framework import serializers
from applications.teams.models import Agent, Role, Team


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ['id', 'team', 'name', 'agents', ]
        read_only_fields = ['agents', ]


class TeamSerializer(serializers.ModelSerializer):

    participants_count = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['id', 'name', 'roles', 'participants_count', ]
        read_only_fields = ['roles', ]

    def get_participants_count(self, obj):
        roles = obj.roles.all().prefetch_related('agents')
        participants_count = 0
        for role in roles:
            participants_count += role.agents.count()
        return participants_count


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ['id', 'team', 'name', 'agents', ]
        read_only_fields = ['agents', ]


class AgentSerializer(serializers.ModelSerializer):

    email = serializers.CharField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = Agent
        fields = ['id', 'first_name', 'last_name', 'email', 'email_confirmed', 'phone_number',
                  'phone_number_confirmed', 'roles', 'user', ]
        read_only_fields = ['first_name', 'last_name', 'email', ]
