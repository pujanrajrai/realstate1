from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('property/desc/<str:pk>', views.property_desc, name='property_desc'),
    path('search/', views.property_search, name='property_search'),
    path('bookmark/', views.bookmark, name='property_bookmark'),
    path('request/', views.request_visit, name='request_visit'),
    path('comment/', views.comment, name='comment'),
    path('mybookmark/', views.my_bookmark, name='my_bookmark'),
    path('myvisitreq/', views.my_visit_req, name='my_visit_req'),
    path('watchlist/remove/', views.remove_watchlist, name="remove_watchlist"),
    path('contactus/', views.contactus, name="contactus"),
]
