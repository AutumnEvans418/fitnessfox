from django.db import models
from model_utils.models import TimeStampedModel as TSModel
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError


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
    
    source_url = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.brand} {self.name}"

class Recipe(TSModel):
    name = models.CharField(max_length=200, blank=False, null=False)
    source_url = models.CharField(max_length=500, blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    servings = models.FloatField(blank=False, null=False, default=1)

    calories = models.FloatField(blank=False, null=False, default=0)
    cholesterol_mg = models.FloatField(blank=False, null=False, default=0)
    sodium_mg = models.FloatField(blank=False, null=False, default=0)
    vitamin_k_mcg = models.FloatField(blank=False, null=False, default=0)

    def set_nutrients(self):
        servings = self.servings

        if servings != 0:
            ingredients = self.recipe_ingredient_set.all()

            self.calories = sum([x.calories for x in ingredients]) / servings
            self.cholesterol_mg = sum([x.cholesterol_mg for x in ingredients]) / servings
            self.sodium_mg = sum([x.sodium_mg for x in ingredients]) / servings
            self.vitamin_k_mcg = sum([x.vitamin_k_mcg for x in ingredients]) / servings

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.set_nutrients()
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
        

class Recipe_Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    servings = models.FloatField(blank=False, null=False)

    calories = models.FloatField(blank=False, null=False, default=0)
    cholesterol_mg = models.FloatField(blank=False, null=False, default=0)
    sodium_mg = models.FloatField(blank=False, null=False, default=0)
    vitamin_k_mcg = models.FloatField(blank=False, null=False, default=0)

    def set_nutrients(self):
        servings = self.servings

        self.calories = self.ingredient.calories * servings
        self.cholesterol_mg = self.ingredient.cholesterol_mg * servings
        self.sodium_mg = self.ingredient.sodium_mg * servings
        self.vitamin_k_mcg = self.ingredient.vitamin_k_mcg * servings

    def save(self,  *args, **kwargs):
        self.set_nutrients()

        self.recipe.save()

        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.recipe.name}---{self.ingredient.name}"

# Create your models here.
class Meal(TSModel):
    BREAKFAST = 0
    LUNCH = 1
    DINNER = 2
    SNACK = 3

    TYPE_CHOICES = [
        (BREAKFAST, 'Breakfast'),
        (LUNCH, 'Lunch'),
        (DINNER, 'Dinner'),
        (SNACK, 'Snack')
    ]

    date = models.DateTimeField(blank=False, null=False, default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    type = models.IntegerField(blank=False, null=False, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.date} {self.user} {self.type}"

class Meal_Recipe(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True, blank=True)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, null=True, blank=True)

    servings = models.FloatField(blank=False, null=False)

    calories = models.FloatField(blank=False, null=False, default=0)
    cholesterol_mg = models.FloatField(blank=False, null=False, default=0)
    sodium_mg = models.FloatField(blank=False, null=False, default=0)
    vitamin_k_mcg = models.FloatField(blank=False, null=False, default=0)

    def set_nutrients(self):
        servings = self.servings

        obj = None
        if self.recipe:
            obj = self.recipe
        else:
            obj = self.ingredient

        self.calories = obj.calories * servings
        self.cholesterol_mg = obj.cholesterol_mg * servings
        self.sodium_mg = obj.sodium_mg * servings
        self.vitamin_k_mcg = obj.vitamin_k_mcg * servings

    def save(self,  *args, **kwargs):
        self.set_nutrients()
        return super().save( *args, **kwargs)
    
    def __str__(self):
        if self.recipe:
            return f"{self.meal} {self.recipe.name}"
        elif self.ingredient:
            return f"{self.meal} {self.ingredient.name}"
        else:
            return f"{self.meal}"

    
    def clean(self):

        if self.recipe is None and self.ingredient is None:
            raise ValidationError("recipe or ingredient must be set")
        if self.recipe is not None and self.ingredient is not None:
            raise ValidationError("recipe and ingredient cannot both be set")

        return super().clean()