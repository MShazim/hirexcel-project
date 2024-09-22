from django.contrib import admin
from django.urls import path , include
from hirexcel_webapp import views

urlpatterns = [
    # -------------------------------------------------- [ START SCREEN ] ---------------------------------------------------------------
    path('', views.start_screen, name='start_screen'),
    # -----------------------------------------------------------------------------------------------------------------------------------

    # -------------------------------------------------- [ LOGIN/ LOGOUT] ---------------------------------------------------------------
    # path('jobseeker_login', views.jobseeker_login, name='jobseeker_login'),
    # path('recruiter_login', views.recruiter_login, name='recruiter_login'),
    # path('jobseeker_logout', views.jobseeker_logout_view, name='jobseeker_logout'),
    # path('recruiter_logout', views.recruiter_logout_view, name='recruiter_logout'),
    path('jobseeker_login', views.jobseeker_login, name='jobseeker_login'),
    path('recruiter_login', views.recruiter_login, name='recruiter_login'),
    path('jobseeker_logout', views.jobseeker_logout_view, name='jobseeker_logout'),
    path('recruiter_logout', views.recruiter_logout_view, name='recruiter_logout'),
    # -----------------------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------- [ HOME ] ------------------------------------------------------------------
    # path('jobseeker_home', views.jobseeker_home, name='jobseeker_home'),
    # path('recruiter_home', views.recruiter_home, name='recruiter_home'),
    path('jobseeker_home', views.jobseeker_home, name='jobseeker_home'),
    path('recruiter_home', views.recruiter_home, name='recruiter_home'),
    # -----------------------------------------------------------------------------------------------------------------------------------

    # ---------------------------------------------- [ JOB POSTS RELATED ] --------------------------------------------------------------
    # path('post_job', views.post_job, name='post_job'),
    # path('get_personality_traits/', views.get_personality_traits, name='get_personality_traits'),
    # path('apply_for_job/<str:job_post_id>/', views.apply_for_job, name='apply_for_job'),
    path('post_job', views.post_job, name='post_job'),
    path('get_personality_traits/', views.get_personality_traits, name='get_personality_traits'),
    path('apply_for_job/<str:job_post_id>/', views.apply_for_job, name='apply_for_job'),
    # -----------------------------------------------------------------------------------------------------------------------------------

    # -------------------------------------------------- [ CREATE ACCOUNT JS] ------------------------------------------------------------
    # path('create-account/job_seeker_create_account_step1/', views.job_seeker_create_account_step1, name='job_seeker_create_account_step1'),
    # path('create-account/job_seeker_create_account_step2/', views.job_seeker_create_account_step2, name='job_seeker_create_account_step2'),
    # path('create-account/job_seeker_create_account_step3/', views.job_seeker_create_account_step3, name='job_seeker_create_account_step3'),
    # path('create-account/job_seeker_create_account_step4/', views.job_seeker_create_account_step4, name='job_seeker_create_account_step4'),
    # path('create-account/success/', views.success_page, name='success_page'),
    path('create-account/job_seeker_create_account_step1/', views.job_seeker_create_account_step1, name='job_seeker_create_account_step1'),
    path('create-account/job_seeker_create_account_step2/', views.job_seeker_create_account_step2, name='job_seeker_create_account_step2'),
    path('create-account/job_seeker_create_account_step3/', views.job_seeker_create_account_step3, name='job_seeker_create_account_step3'),
    path('create-account/job_seeker_create_account_step4/', views.job_seeker_create_account_step4, name='job_seeker_create_account_step4'),
    path('create-account/success/', views.success_page, name='success_page'),
    # -----------------------------------------------------------------------------------------------------------------------------------

    # -------------------------------------------------- [ CREATE ACCOUNT R] ------------------------------------------------------------
    # path('create-account/recruiter-step1/', views.recruiter_create_account_step1, name='recruiter_create_account_step1'),
    # path('create-account/recruiter-step2/', views.recruiter_create_account_step2, name='recruiter_create_account_step2'),
    # path('create-account/recruiter_success/', views.recruiter_success_page, name='recruiter_success_page'),
    path('create-account/recruiter-step1/', views.recruiter_create_account_step1, name='recruiter_create_account_step1'),
    path('create-account/recruiter-step2/', views.recruiter_create_account_step2, name='recruiter_create_account_step2'),
    path('create-account/recruiter_success/', views.recruiter_success_page, name='recruiter_success_page'),
    # -----------------------------------------------------------------------------------------------------------------------------------

    # -------------------------------------------------- [ QUIZ START] ------------------------------------------------------------------
    path('quiz_start_screen', views.quiz_start_screen, name='quiz_start_screen'),
    # ----------------------------[ DISC QUIZ ]--------------------------------------------------
    path('disc_quiz/start/', views.disc_quiz_start, name='disc_quiz_start'),
    path('disc_quiz/<str:question_id>/', views.disc_quiz, name='disc_quiz'),
    path('disc_quiz/', views.disc_quiz_start_redirect, name='disc_quiz_start_redirect'),
    path('phase_one_completed', views.phase_one_completed, name='phase_one_completed'),
    # -------------------------------------------------------------------------------------------


    # ----------------------------[ NON VERBAL QUIZ ]--------------------------------------------------
    path('non_verbal_quiz/start/', views.non_verbal_quiz_start, name='non_verbal_quiz_start'),
    path('non_verbal_quiz/<int:question_index>/', views.non_verbal_quiz, name='non_verbal_quiz'),
    path('non_verbal_quiz/', views.non_verbal_quiz_start_redirect, name='non_verbal_quiz_start_redirect'),
    path('phase_two_completed', views.phase_two_completed, name='phase_two_completed'),
    # -------------------------------------------------------------------------------------------------

    # ----------------------------[ TECHNICAL QUIZ ]--------------------------------------------------
    path('technical_quiz/start/', views.technical_quiz_start, name='technical_quiz_start'),
    path('technical_quiz/<int:question_index>/', views.technical_quiz, name='technical_quiz'),
    path('technical_quiz/', views.technical_quiz_start_redirect, name='technical_quiz_start_redirect'),
    path('phase_three_completed', views.phase_three_completed, name='phase_three_completed'),
    # -------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------------------------
]
