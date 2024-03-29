# Generated by Django 5.0.3 on 2024-03-24 23:07

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0014_alter_groupmember_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupmember',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
        migrations.AlterField(
            model_name='usergroup',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
