# Generated by Django 4.2.11 on 2024-05-28 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.CharField(max_length=220, verbose_name='correo electronico'),
        ),
    ]