# Generated by Django 5.0.3 on 2024-03-13 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0011_groupmessage_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupmessage',
            name='created_at',
        ),
    ]
