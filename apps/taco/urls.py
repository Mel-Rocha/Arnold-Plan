from django.urls import path
from .views import CMVColtaco3ListView, CMVColtaco3DetailView, CMVColtaco3CategoryView, CMVColtaco3BulkDetailView

urlpatterns = [
    path('taco/', CMVColtaco3ListView.as_view(), name='taco-list'),
    path('taco/category/<str:category>/', CMVColtaco3CategoryView.as_view(), name='taco-category'),
    path('taco/<str:param>/<str:amount>/', CMVColtaco3DetailView.as_view(), name='taco-detail'),
    path('bulk-detail/<str:food_list>/', CMVColtaco3BulkDetailView.as_view(), name='taco-bulk-detail'),

]
