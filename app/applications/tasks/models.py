from django.db import models
from django.contrib.auth import get_user_model

from applications.teams.models import Agent


User = get_user_model()


class Task(models.Model):

    class StatusTextField(models.TextChoices):
        STARTED = 'started'
        IN_PROGRESS = 'in progress'
        COMPLETED = 'completed'

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_tasks')
    assigned_to = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, related_name='tasks')
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(null=True)
    status = models.CharField(max_length=32, choices=StatusTextField.choices, default=StatusTextField.STARTED)
