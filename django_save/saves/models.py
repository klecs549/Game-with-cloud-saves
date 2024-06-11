from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.

class Save(models.Model):
    name = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.JSONField(null=True, blank=True)
