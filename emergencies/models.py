from django.db import models

# Create your models here.
class myModel(models.Model):
    name = models.CharField(max_length=220)
    password = models.CharField(max_length=200, null=True)