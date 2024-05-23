from django.contrib import admin
from django.urls import path , include
from hirexcel_webapp import views

urlpatterns = [
    path('', views.start_screen, name='start_screen'),
    path('jobseeker_login', views.jobseeker_login, name='jobseeker_login'),
    path('recruiter_login', views.recruiter_login, name='recruiter_login'),
    path('jobseeker_create_account', views.jobseeker_create_account, name='jobseeker_create_account'),
    path('recruiter_create_account', views.recruiter_create_account, name='recruiter_create_account'),
    path('jobseeker_home', views.jobseeker_home, name='jobseeker_home'),
    path('recruiter_home', views.recruiter_home, name='recruiter_home'),
    path('post_job', views.post_job, name='post_job'),
    path('quiz_start_screen', views.quiz_start_screen, name='quiz_start_screen'),
]
