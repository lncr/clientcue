from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Tag(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags')
    contacts = models.ManyToManyField('contacts.Contact', related_name='tags')
    name = models.CharField(max_length=255)
