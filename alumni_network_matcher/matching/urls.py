from django.urls import path
from . import views

urlpatterns = [
    path('', views.find_mentors, name='find_mentors'),
    path('mentor/<int:pk>/', views.mentor_detail, name='mentor_detail'),
]