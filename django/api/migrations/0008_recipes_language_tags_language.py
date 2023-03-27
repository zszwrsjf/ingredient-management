# Generated by Django 4.1.2 on 2022-11-06 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0007_remove_recipes_language_remove_tags_language"),
    ]

    operations = [
        migrations.AddField(
            model_name="recipes",
            name="language",
            field=models.CharField(
                choices=[
                    ("en", "english"),
                    ("sp", "spanish"),
                    ("ch", "chinese"),
                    ("gm", "german"),
                    ("jp", "japanese"),
                    ("kr", "korean"),
                    ("hb", "hebrew"),
                ],
                default="en",
                max_length=2,
            ),
        ),
        migrations.AddField(
            model_name="tags",
            name="language",
            field=models.CharField(
                choices=[
                    ("en", "english"),
                    ("sp", "spanish"),
                    ("ch", "chinese"),
                    ("gm", "german"),
                    ("jp", "japanese"),
                    ("kr", "korean"),
                    ("hb", "hebrew"),
                ],
                default="en",
                max_length=2,
            ),
        ),
    ]
