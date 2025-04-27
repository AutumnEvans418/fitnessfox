from django.contrib import admin

from .models import Ingredient, Recipe, Recipe_Ingredient, Meal, Meal_Recipe
# Register your models here.

admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(Recipe_Ingredient)
admin.site.register(Meal)
admin.site.register(Meal_Recipe)