from django.contrib import admin

from apps.macros_sheet.models import MacrosSheet


@admin.register(MacrosSheet)
class MacrosSheetAdmin(admin.ModelAdmin):
    list_display = ('diet', 'week', 'kcal', 'cho', 'ptn', 'fat', 'kcal_level', 'cho_proportion',
                    'ptn_proportion', 'fat_proportion')
    search_fields = ('macros_planner__athlete__name', 'macros_planner__nutritionist__name', 'week')
    readonly_fields = ('kcal', 'kcal_level', 'cho_proportion', 'ptn_proportion', 'fat_proportion')
    fieldsets = (
        (None, {'fields': ('diet', 'week')}),
        ('Macros', {'fields': ('cho', 'ptn', 'fat', 'kcal', 'kcal_level', 'cho_proportion', 'ptn_proportion',
                               'fat_proportion')}),
    )
