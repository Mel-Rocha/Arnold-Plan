from django.urls import path
from .views import CMVColtaco3ListView, CMVColtaco3DetailView, CMVColtaco3CategoryView

urlpatterns = [
    path('taco/', CMVColtaco3ListView.as_view(), name='taco-list'),
    path('taco/<str:param>/', CMVColtaco3DetailView.as_view(), name='taco-detail'),
    path('taco/category/<str:category>/', CMVColtaco3CategoryView.as_view(), name='taco-category'),
]
