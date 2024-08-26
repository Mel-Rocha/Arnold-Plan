from django.contrib import admin

from apps.food_options.models import FoodOptions


@admin.register(FoodOptions)
class FoodOptionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'meal', 'food', 'quantity', 'unit_of_measurement')
    list_filter = ('meal', 'unit_of_measurement')
    search_fields = ('food',)
    ordering = ('meal', 'food')

    fieldsets = (
        (None, {
            'fields': ('meal', 'food', 'quantity', 'unit_of_measurement')
        }),
    )
