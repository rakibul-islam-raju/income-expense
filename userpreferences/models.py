from django.db import models
from django.contrib.auth.models import User


class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userpreferences')
    currency = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username
    