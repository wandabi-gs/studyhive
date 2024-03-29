# Generated by Django 3.2.24 on 2024-02-14 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interest', '0004_alter_recommendation_source'),
        ('chat', '0002_auto_20240214_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='usergroup',
            name='interests',
            field=models.ManyToManyField(related_name='group_interests', to='interest.Interest'),
        ),
    ]
