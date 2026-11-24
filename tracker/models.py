from django.db import models


class Issue(models.Model):
    title = models.CharField(max_length=120)
    location = models.CharField(max_length=100)
    resolved = models.BooleanField(default=False)
