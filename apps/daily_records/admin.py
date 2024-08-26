from django.contrib import admin

from apps.daily_records.models import DailyRecords


@admin.register(DailyRecords)
class DailyRecordsAdmin(admin.ModelAdmin):
    list_display = (
        'athlete',
        'date',
        'morning_meal',
        'afternoon_meal',
        'evening_meal',
        'bowel_movements',
        'hunger_times',
        'stress_times',
        'anxiety_times',
        'craving_times'
    )
    list_filter = (
        'date',
        'morning_meal',
        'afternoon_meal',
        'evening_meal',
        'hunger_times',
        'stress_times',
        'anxiety_times',
        'craving_times'
    )
    search_fields = (
        'athlete__name',
        'date'
    )
    ordering = ('-date',)

    fieldsets = (
        (None, {
            'fields': ('athlete', 'date')
        }),
        ('Meals', {
            'fields': ('morning_meal', 'afternoon_meal', 'evening_meal')
        }),
        ('Daily Records', {
            'fields': ('bowel_movements', 'hunger_times', 'stress_times', 'anxiety_times', 'craving_times')
        }),
    )
