# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_room/', views.create_room, name="create_room"),
    path('<str:room_name>/<str:username>/', views.room, name='room'),
]