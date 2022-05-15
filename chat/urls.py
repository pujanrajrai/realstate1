from django.urls import path
from . import views

app_name = 'chats'

urlpatterns = [
    path('all/chat', views.all_chat, name='chat'),
    path('view/<slug:username>', views.view_chat, name='view_chat'),
    path('new/message/<str:username>', views.new_chat, name='new_message')
]
