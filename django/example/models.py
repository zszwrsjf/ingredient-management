from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField(validators=[MinValueValidator(0)])
    summary = models.TextField()
