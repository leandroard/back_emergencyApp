# Generated by Django 4.2.11 on 2024-05-28 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_users_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='phone_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
