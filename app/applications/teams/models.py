from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Team(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='teams')
    name = models.CharField(max_length=255)


class Role(models.Model):
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name='roles')
    name = models.CharField(max_length=255)


class Agent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agents')
    phone_number = models.CharField(max_length=128, blank=True)
    roles = models.ManyToManyField(Role, related_name='agents')
    email_confirmed = models.BooleanField(default=False)
    phone_number_confirmed = models.BooleanField(default=False)
