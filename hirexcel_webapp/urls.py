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
    path('get_personality_traits/', views.get_personality_traits, name='get_personality_traits'),


    path('quiz_start_screen', views.quiz_start_screen, name='quiz_start_screen'),

    path('disc_quiz/<int:question_id>/', views.disc_quiz, name='disc_quiz'),
    path('disc_quiz/', views.disc_quiz, {'question_id': 1}, name='disc_quiz_start'),
    path('phase_one_completed', views.phase_one_completed, name='phase_one_completed'),

    path('non_verbal_quiz/<int:question_index>/', views.non_verbal_quiz, name='non_verbal_quiz'),
    path('non_verbal_quiz/', views.non_verbal_quiz, {'question_index': 0}, name='non_verbal_quiz_start'),
    path('phase_two_completed', views.phase_two_completed, name='phase_two_completed'),


    path('technical_quiz/<int:question_index>/', views.technical_quiz, name='technical_quiz'),
    path('technical_quiz/', views.technical_quiz, {'question_index': 0}, name='technical_quiz_start'),
    path('phase_three_completed', views.phase_three_completed, name='phase_three_completed'),
]
