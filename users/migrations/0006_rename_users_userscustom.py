# Generated by Django 4.2.11 on 2024-05-28 03:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_users_options'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Users',
            new_name='UsersCustom',
        ),
    ]
