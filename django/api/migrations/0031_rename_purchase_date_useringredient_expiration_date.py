# Generated by Django 4.1.2 on 2022-11-19 05:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0030_remove_recipeingredient_ingredient_quantity_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="useringredient",
            old_name="purchase_date",
            new_name="expiration_date",
        ),
    ]
