from django.contrib import admin
from django.urls import path , include
from hirexcel_webapp import views

urlpatterns = [
    path('', views.start_screen, name='start_screen'),
    path('login', views.login, name='login')
]
