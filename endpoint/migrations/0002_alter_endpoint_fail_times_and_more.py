# Generated by Django 4.1.5 on 2023-01-21 22:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('endpoint', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endpoint',
            name='fail_times',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterUniqueTogether(
            name='endpoint',
            unique_together={('user', 'endpoint')},
        ),
    ]
