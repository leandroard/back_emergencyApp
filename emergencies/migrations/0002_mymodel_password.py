# Generated by Django 4.2.11 on 2024-05-28 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emergencies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mymodel',
            name='password',
            field=models.CharField(max_length=200, null=True),
        ),
    ]