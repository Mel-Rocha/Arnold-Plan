from django.contrib import admin

from apps.user.models import User, Athlete, Nutritionist


# User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_nutritionist', 'is_athlete', 'is_staff', 'is_active')
    list_filter = ('is_nutritionist', 'is_athlete', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_nutritionist', 'is_athlete')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active',
                       'is_nutritionist', 'is_athlete'),
        }),
    )

# Athlete
@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'weight', 'height', 'birth_date', 'is_pro', 'nutritionist')
    list_filter = ('category', 'is_pro', 'nutritionist')
    search_fields = ('name', 'category')
    ordering = ('name',)
    fieldsets = (
        (None, {'fields': ('user', 'name', 'gender', 'instagram', 'email', 'telephone')}),
        ('Athlete Information', {'fields': ('category', 'weight', 'height', 'birth_date', 'is_pro', 'nutritionist')}),
    )

# Nutritionist
@admin.register(Nutritionist)
class NutritionistAdmin(admin.ModelAdmin):
    list_display = ('name', 'crn', 'academic_degree', 'area_of_specialization')
    list_filter = ('academic_degree', 'area_of_specialization')
    search_fields = ('name', 'crn')
    ordering = ('name',)
    fieldsets = (
        (None, {'fields': ('user', 'name', 'gender', 'instagram', 'email', 'telephone')}),
        ('Professional Information', {'fields': ('crn', 'academic_degree', 'area_of_specialization')}),
    )
