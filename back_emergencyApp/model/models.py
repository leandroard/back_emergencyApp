from django.db import models
class Usuarios(models.Model):
     nombre = models.CharField(max_length=200),
     apellido = models.CharField(max_length=100),
     correo = models.CharField(EmailField=100)
     