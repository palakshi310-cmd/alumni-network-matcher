from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_connections, name='my_connections'),
    path('send/<int:mentor_id>/', views.send_connection_request, name='send_connection_request'),
    path('handle/<int:connection_id>/<str:action>/', views.handle_request, name='handle_request'),
]