# Generated by Django 4.1.2 on 2022-11-19 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0027_alter_ingredient_freezer_days_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="title",
            field=models.CharField(max_length=64),
        ),
    ]