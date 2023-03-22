# Generated by Django 4.1.7 on 2023-03-22 06:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("news", "0004_alter_category_article"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="category",
            name="article",
        ),
        migrations.AddField(
            model_name="newsarticle",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="categories",
                to="news.category",
            ),
        ),
    ]
