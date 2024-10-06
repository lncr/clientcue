from django.db import models


class Industry(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Industry"
        verbose_name_plural = "Industries"

    def __str__(self):
        return f'{self.title}'
