from django.db import models
from users.models import User

class EmergencyType(models.Model):
    name = models.CharField(max_length=220)
    icon = models.ImageField()

    class Meta:
        verbose_name = "Tipo de Emergencia"
        verbose_name_plural = "Tipos de Emergencias"

    def __str__(self) -> str:
        return self.name


class Emergency(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    emergency_type = models.ForeignKey(EmergencyType, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
    )
    created_at = models.DateTimeField(auto_now_add=True, )

    def __str__(self) -> str:
        return self.emergency_type

    class Meta:
        verbose_name = 'emergency'
        verbose_name_plural = 'emergencies'
