# Generated by Django 4.1.2 on 2022-11-06 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0011_rename_tag_id_recipetag_tag_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipenutrition",
            name="recipe_id",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="api.recipe"
            ),
        ),
    ]