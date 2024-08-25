from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
import random

class Role(models.Model):
    CIUDADANO = 'ciudadano'
    POLICIA = 'policia'
    AMBULANCIA = 'ambulancia'
    BOMBEROS = 'bomberos'

    ROLE_CHOICES = [
        (CIUDADANO, _('Ciudadano')),
        (POLICIA, _('Policía')),
        (AMBULANCIA, _('Ambulancia')),
        (BOMBEROS, _('Bomberos')),
    ]

    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()

    class Meta:
        verbose_name = _('Rol')
        verbose_name_plural = _('Roles')



class User(AbstractUser):
    email = models.EmailField(unique=True)
    number_id = models.IntegerField(unique=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')

    def __str__(self):
        return self.email

    @property
    def role_name(self):
        return self.role.get_name_display() if self.role else None

  
class EmergencyRoleModel(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_PENDING, _('Pending')),
        (STATUS_APPROVED, _('Approved')),
        (STATUS_REJECTED, _('Rejected')),
    ]

    user = models.ForeignKey('User', on_delete=models.CASCADE)
    requested_role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='emergency_role_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    number_id = models.CharField(max_length=20)
    plate_vehicle = models.CharField(max_length=10)
    adress = models.CharField(max_length=255)

    def clean(self):
        if not self.pk:  # Nuevo objeto
            if EmergencyRoleModel.objects.filter(user=self.user, status=self.STATUS_PENDING).exists():
                raise ValidationError(_("User already has a pending role change request."))
        elif self.status == self.STATUS_APPROVED and self._state.adding is False:
            original = EmergencyRoleModel.objects.get(pk=self.pk)
            if original.status != self.STATUS_APPROVED:
                self.user.role = self.requested_role
                self.user.save()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @classmethod
    def approve_request(cls, request_id):
        try:
            request = cls.objects.get(id=request_id, status=cls.STATUS_PENDING)
            request.status = cls.STATUS_APPROVED
            request.save()
            return True
        except cls.DoesNotExist:
            return False

    @classmethod
    def reject_request(cls, request_id):
        try:
            request = cls.objects.get(id=request_id, status=cls.STATUS_PENDING)
            request.status = cls.STATUS_REJECTED
            request.save()
            return True
        except cls.DoesNotExist:
            return False

class CodeRecoverPassword(models.Model):
    code = models.IntegerField(verbose_name=_('Código de seguridad'), null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField(verbose_name=_('Tiempo válido del código'), null=False)

    class Meta:
        verbose_name = _('Código de seguridad restablecimiento de contraseña')
        verbose_name_plural = _('Códigos de seguridad restablecimiento de contraseñas')

    def __str__(self):
        return f"Code for {self.user.email}"