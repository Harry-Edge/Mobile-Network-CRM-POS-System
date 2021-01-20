from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginPage, name='root'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('menu/', views.menu, name='menu'),
]
