from django.db import models

class UsersCustom(models.Model):
    user=  models.CharField(max_length=200, null=True)
    phone_number = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=220 , verbose_name="correo electronico")

    class Meta:
        verbose_name = "Mis usuraios"
        verbose_name_plural = "Mis usureaios"