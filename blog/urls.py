from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('delete/<blog_id>/', views.delete, name='delete'),
    path('edit/<int:blog_id>/', views.edit, name='edit'),
]
