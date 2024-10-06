from datetime import date
from rest_framework import serializers

from applications.tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):

    ticket_number = serializers.CharField(source='id', read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'assigned_to', 'ticket_number', 'description', 'deadline', 'status', ]

    def validate_deadline(self, value):
        if value < date.today():
            raise serializers.ValidationError('Deadline cannot be in the past')
        return value
