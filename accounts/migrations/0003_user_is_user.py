# Generated by Django 4.1.7 on 2023-03-16 09:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_user_is_editor"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_user",
            field=models.BooleanField(default=True),
        ),
    ]