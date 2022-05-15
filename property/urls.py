from django.urls import path
from . import views

app_name = 'property'

urlpatterns = [
    # property category
    path('category/create/', views.PropertyCategoryCreateView.as_view(), name='property_category_create'),
    path('category/list/', views.PropertyCategoryListView.as_view(), name='property_category_list'),
    path('category/update/<str:pk>', views.PropertyCategoryUpdateView.as_view(), name='property_category_update'),

    # property
    path('create/', views.PropertyCreateView.as_view(), name='property_create'),
    path('update/<str:pk>', views.PropertyUpdateView.as_view(), name='property_update'),
    path('list/', views.PropertyListView.as_view(), name='property_list'),


]
