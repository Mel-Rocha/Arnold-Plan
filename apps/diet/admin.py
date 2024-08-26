from django.contrib import admin

from apps.diet.models import Diet
from apps.meal.models import Meal


class MealInline(admin.TabularInline):
    model = Meal
    extra = 1

@admin.register(Diet)
class DietAdmin(admin.ModelAdmin):
    list_display = ('id', 'athlete', 'nutritionist', 'goal', 'initial_date', 'final_date', 'type_of_diet')
    list_filter = ('type_of_diet', 'initial_date', 'final_date', 'macros_planner__athlete',
                   'macros_planner__nutritionist')
    search_fields = ('goal', 'observations')
    ordering = ('initial_date',)
    inlines = [MealInline]

    fieldsets = (
        (None, {
            'fields': ('macros_planner', 'goal', 'observations', 'initial_date', 'final_date', 'weeks', 'type_of_diet')
        }),
    )
