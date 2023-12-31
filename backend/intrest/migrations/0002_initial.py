# Generated by Django 4.2.4 on 2023-09-05 09:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("intrest", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="userreview",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="userinterest",
            name="interests",
            field=models.ManyToManyField(to="intrest.interest"),
        ),
        migrations.AddField(
            model_name="userinterest",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_intrests",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="interest",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="intrests",
                to="intrest.category",
            ),
        ),
        migrations.AddField(
            model_name="interest",
            name="recommendations",
            field=models.ManyToManyField(to="intrest.recommendation"),
        ),
    ]
