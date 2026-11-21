from django.urls import path
from django.contrib.auth import views as auth_views
from . import views as accounts_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        redirect_authenticated_user=True,
        next_page='dashboard'
    ), name='login'),
    
    # path('logout/', auth_views.LogoutView.as_view(
    #     next_page='home', 
    #     template_name='accounts/logged_out.html'  # Optional
    # ), name='logout'),
    
    path('register/', accounts_views.register, name='register'),
    path('logout/', accounts_views.custom_logout, name='logout'),
]