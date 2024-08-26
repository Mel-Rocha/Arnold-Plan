import functools

from drf_yasg import openapi
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view


def swagger_safe(model):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if getattr(self, 'swagger_fake_view', False):
                return model.objects.none()
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


schema_view = get_schema_view(
    openapi.Info(
        title="Arnold Plan",
        default_version='v0 - Minimum Viable Product',
        description="End-points for the Arnold Plan API in Django Rest",
        terms_of_service="terms",
        contact=openapi.Contact(email="rochamel73@gmail.com"),
        license=openapi.License(name="MIT License"),
        ),
    public=True,
    permission_classes=(permissions.BasePermission,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-ui'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('user/', include('apps.user.urls')),
    path('daily-records/', include('apps.daily_records.urls')),
    path('diet/', include('apps.diet.urls')),
    path('macros-planner/', include('apps.macros_planner.urls')),
    path('macros-sheet/', include('apps.macros_sheet.urls')),
    path('meal/', include('apps.meal.urls')),
    path('food_options/', include('apps.food_options.urls')),
    ]
