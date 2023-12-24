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
     
    path('borrow-book/<str:book_id>/', views.borrow_book, name='borrow-book'),
    # When user clicks borrow in the dashboard

    path('search/', views.search_books, name='search_books'),
    # When user clicks search in the dashboard
    
    path('searchGuest/', views.search_books_guest, name='search_books_guest'),
    # When guest clicks search in the dashboard
    
    path('DashboardGuest', views.dashboard_guest, name='DashboardGuest'),
    # When guest clicks search in the start

    path('updateMember/', views.update_member, name='update_member'),
    # When user clicks update account in the settings

    path('delete_account/', views.delete_account, name='delete_account'),
     # When user clicks delete account in the settings

    # when user clicks on the preview button on the guest dashboard
     path('PreviewBookGuest/<str:book_id>/', views.preview_book_guest, name='preview_book_guest'),

     # when user clicks on the preview button on the guest dashboard
     path('PreviewBook.html/<str:book_id>/', views.preview_book, name='preview_book'),

    # when an admin clicks on the borrowing records navigation on the admin dashboard
    path('UserRecords',views.user_records, name='UserRecords'),

    # when an admin clicks on return
    path('return-book/<str:record_id>/', views.return_book, name='return-book'),

    #when an admin clicks the paid button
    path('pay-penalty/<str:record_id>/', views.pay_penalty, name='return-book'),

    #When member clicks the penalty link
    path('Penalties', views.penalties, name='penalties'),

    #When member clicks the extend button
    path('extend/<str:record_id>/', views.extend_return_date, name='extend_return_date'),

]