# Generated by Django 4.1.2 on 2022-11-06 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_remove_recipes_language"),
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
        migrations.AlterField(
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
