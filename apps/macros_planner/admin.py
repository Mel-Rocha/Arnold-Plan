from django.contrib import admin

from apps.macros_sheet.models import MacrosSheet
from apps.macros_planner.models import MacrosPlanner


class MacrosSheetInline(admin.TabularInline):
    model = MacrosSheet
    extra = 1
    readonly_fields = ('kcal', 'kcal_level', 'cho_proportion', 'ptn_proportion', 'fat_proportion')
    can_delete = True

@admin.register(MacrosPlanner)
class MacrosPlannerAdmin(admin.ModelAdmin):
    list_display = ('athlete', 'nutritionist', 'goal', 'initial_date', 'final_date', 'weeks')
    inlines = [MacrosSheetInline]
    search_fields = ('athlete__name', 'nutritionist__name')
    list_filter = ('initial_date', 'final_date', 'nutritionist')

    fieldsets = (
        (None, {'fields': ('athlete', 'nutritionist')}),
        ('Planning', {'fields': ('goal', 'initial_date', 'final_date', 'weeks')}),
    )
