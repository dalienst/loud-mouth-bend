# Generated by Django 4.1.7 on 2023-03-29 12:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("news", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="newspaper",
            name="created_by",
            field=models.ForeignKey(
                default="9d80b140-8e88-420c-b043-410b33a6181d",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="newspaper",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
