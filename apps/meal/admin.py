from django.contrib import admin

from apps.meal.models import Meal


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('id', 'diet', 'name', 'time', 'type_of_meal')
    list_filter = ('type_of_meal', 'time', 'diet')
    search_fields = ('name',)
    ordering = ('time',)

    fieldsets = (
        (None, {
            'fields': ('diet', 'name', 'time', 'type_of_meal')
        }),
    )
