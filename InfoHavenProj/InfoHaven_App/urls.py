from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('',views.home, name="home"),

    # Define URL patterns for the InfoHaven pages.

    path('Register', views.register, name="Register"),
    # When a user visits '/Register', Django will call the 'register' view.

    path('Login', views.login, name="Login"),
    # When a user visits '/Login', Django will call the 'login' view.

    path('Start', views.start, name="Start"),
    # When a user visits '/start', Django will call the 'start' view.

    path('Start_Logged', views.start_logged, name="Start_Logged"),
    # When a user visits '/start', Django will call the 'start_logged' view.

    path('Logout',views.logout,name="Logout"),
    # When a user visits '/start', Django will call the 'logout' view.

    path('Dashboard',views.dashboard,name="Dashboard"),
    # When a user visits '/Dashboard', Django will call the 'dashboard' view.

    path('DashboardAdmin',views.dashboard_admin, name="DashboardAdmin"),
     # When a user visits '/DashboardAdmin', Django will call the 'dashboard_admin' view.

    path('update_book/<str:book_id>/', views.update_book, name='update_book'),
     # When user clicks update

    path('delete_book/<str:book_id>/', views.delete_book, name='delete_book'),
     # When user clicks delete

    path('add_book/', views.add_book, name='add_book'),
     # When user clicks add new book

    path('profile/', views.profile, name='profile'),
     # When user clicks view profile
     
    path('borrow_book/<str:book_id>/', views.borrow_book, name='borrow_book'),
    # When user clicks borrow in the dashboard
]