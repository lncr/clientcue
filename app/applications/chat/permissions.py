from rest_framework.permissions import BasePermission


class MessageDetailPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        if obj.chat_room:
            team = obj.chat_room.team
            agents = user.agents.all()
            if team.owner_id == user.id:
                return True
            is_user_in_team = False
            for agent in agents:
                roles = agent.roles.all()
                for role in roles:
                    if role.team_id == team.id:
                        is_user_in_team = True
                        break
            return is_user_in_team

        else:
            return obj.recipient_id == user.id or obj.sender_id == user.id
