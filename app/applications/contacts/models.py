from django.contrib.auth import get_user_model
from django.db import models
from applications.companies.models import Mark


User = get_user_model()


class Contact(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    phone_number = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    rating = models.PositiveSmallIntegerField(choices=Mark.marks)
