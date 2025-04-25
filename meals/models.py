from django.db import models
from model_utils.models import TimeStampedModel as TSModel
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone


class Ingredient(TSModel):
    OZ = 0
    CUP = 1
    TSP = 2
    GRAMS = 3
    ITEMS = 4
    TBSP = 5

    SERVING_UNIT_CHOICES = [
        (OZ, 'Ounces'),
        (CUP, 'Cups'),
        (TSP, 'Tsps'),
        (GRAMS, 'Grams'),
        (ITEMS, 'Items'),
        (TBSP, 'Tbsps')
    ]

    name = models.CharField(max_length=200, blank=False, null=False)
    brand = models.CharField(max_length=200, blank=False, null=False)
    serving_size = models.FloatField(blank=False, null=False)
    serving_unit = models.IntegerField(blank=False, null=False, choices=SERVING_UNIT_CHOICES)

    calories = models.FloatField(blank=False, null=False, default=0)
    cholesterol_mg = models.FloatField(blank=False, null=False, default=0)
    sodium_mg = models.FloatField(blank=False, null=False, default=0)
    vitamin_k_mcg = models.FloatField(blank=False, null=False, default=0)
    
    source_url = models.CharField(max_length=500)

class Recipe(TSModel):
    name = models.CharField(max_length=200, blank=False, null=False)
    source_url = models.CharField(max_length=500)
    author = models.CharField(max_length=100)

    

# Create your models here.
class Meal(TSModel):
    date = models.DateTimeField(blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
