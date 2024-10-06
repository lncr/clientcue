from django.db import models

from applications.industries.models import Industry
from applications.users.models import User
from django.contrib.auth import get_user_model

class Company(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    industry = models.ForeignKey(Industry, on_delete=models.PROTECT, related_name='industry_company')
    directors = models.ManyToManyField(User, related_name='director_companies', blank=True)
    managers = models.ManyToManyField(User, related_name='manager_companies', blank=True)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return f'{self.name} {self.industry}'

User = get_user_model()

class Mark:
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    marks = ((one, 'Too bad!'), (two, 'Bad!'), (three, 'Normal!'),
             (four, 'Good!'), (five, 'Excellent!'))

class Review(models.Model):
    product = models.ForeignKey(Company, on_delete=models.CASCADE,
                                related_name='reviews')
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=Mark.marks)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
