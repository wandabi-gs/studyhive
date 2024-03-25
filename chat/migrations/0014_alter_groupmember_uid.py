# Generated by Django 5.0.3 on 2024-03-24 23:07

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0013_alter_usergroup_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupmember',
            name='uid',
            field=models.CharField(default=uuid.uuid4, max_length=30, unique=True),
        ),
    ]