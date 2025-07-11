from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('rooms/', views.room_list, name='room_list'),
    path('room/<int:id>/', views.room_detail, name='room_detail'),  
    path('room/<int:id>/send_message/', views.send_message, name='send_message'),
    path('create_room/', views.create_room, name='create_room'),
    path('room/<int:room_id>/messages/', views.get_messages, name='get_messages'),
]
