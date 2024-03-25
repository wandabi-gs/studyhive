# Generated by Django 5.0.3 on 2024-03-17 13:15

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interest', '0012_alter_recommendationvideo_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='uid',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='interest',
            name='uid',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='uid',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='recommendationnotes',
            name='uid',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='recommendationvideo',
            name='uid',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='usercontent',
            name='uid',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='userinterest',
            name='uid',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='userrecommendation',
            name='uid',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=50, unique=True),
        ),
    ]