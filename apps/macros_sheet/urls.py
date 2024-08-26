from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.macros_sheet.views import MacrosSheetViewSet

router = DefaultRouter()
router.register(
    r'macros-planners/(?P<macros_planner_id>[0-9a-f-]{36})/macros-sheets',
    MacrosSheetViewSet,
    basename='macros-sheet'
)


urlpatterns = [
    path('', include(router.urls)),
]
