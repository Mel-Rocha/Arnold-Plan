from django.contrib import admin

from apps.meal.models import Meal
from apps.food_options.models import FoodOptions


class FoodOptionsInline(admin.TabularInline):
    model = FoodOptions
    extra = 1

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('id', 'diet', 'name', 'time', 'type_of_meal')
    list_filter = ('type_of_meal', 'time', 'diet')
    search_fields = ('name',)
    ordering = ('time',)
    inlines = [FoodOptionsInline]

    fieldsets = (
        (None, {
            'fields': ('diet', 'name', 'time', 'type_of_meal')
        }),
    )
