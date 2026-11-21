from django.urls import path
from . import views

urlpatterns = [
    path('with/<int:connection_id>/', views.chat_room, name='chat_room'),
]