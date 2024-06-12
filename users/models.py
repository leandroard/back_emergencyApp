from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email


class CodeRecoverPassword(models.Model):
    code = models.IntegerField(verbose_name=_('Codigo de seguridad'), null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_created=True)
    expiration = models.DateTimeField(verbose_name=_('tiempo de valido  del codigo'), null=False)

    class Meta:
        verbose_name = _('Codigo de seguridad restablecimiento de contraseña')
        verbose_name_plural = _('Codigos de seguridad restablecimiento de contraseñas')