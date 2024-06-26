# Generated by Django 5.0.3 on 2024-04-01 13:27

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_alter_customuser_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connection',
            name='uid',
            field=models.CharField(default=uuid.uuid4, max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='uid',
            field=models.CharField(default=uuid.uuid4, max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='reporteduser',
            name='uid',
            field=models.CharField(default=uuid.uuid4, max_length=50, unique=True),
        ),
    ]
