from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_book, name='add_book'),
    path('remove/<int:book_id>/', views.remove_book, name='remove_book'),
    path('edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('', views.book_list, name='book_list'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
]