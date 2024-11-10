from django.test import SimpleTestCase
from django.urls import reverse, resolve
from hirexcel_webapp import views

class TestUrls(SimpleTestCase):
    
    def test_start_screen_url(self):
        url = reverse('start_screen')
        self.assertEqual(resolve(url).func, views.start_screen)

    def test_jobseeker_login_url(self):
        url = reverse('jobseeker_login')
        self.assertEqual(resolve(url).func, views.jobseeker_login)

    def test_recruiter_login_url(self):
        url = reverse('recruiter_login')
        self.assertEqual(resolve(url).func, views.recruiter_login)

    def test_jobseeker_logout_url(self):
        url = reverse('jobseeker_logout')
        self.assertEqual(resolve(url).func, views.jobseeker_logout_view)

    def test_recruiter_logout_url(self):
        url = reverse('recruiter_logout')
        self.assertEqual(resolve(url).func, views.recruiter_logout_view)

    def test_jobseeker_home_url(self):
        url = reverse('jobseeker_home')
        self.assertEqual(resolve(url).func, views.jobseeker_home)

    def test_recruiter_home_url(self):
        url = reverse('recruiter_home')
        self.assertEqual(resolve(url).func, views.recruiter_home)

    def test_post_job_url(self):
        url = reverse('post_job')
        self.assertEqual(resolve(url).func, views.post_job)

    def test_get_personality_traits_url(self):
        url = reverse('get_personality_traits')
        self.assertEqual(resolve(url).func, views.get_personality_traits)

    def test_apply_for_job_url(self):
        url = reverse('apply_for_job', args=['test_job_id'])
        self.assertEqual(resolve(url).func, views.apply_for_job)

    def test_job_seeker_create_account_url(self):
        url = reverse('job_seeker_create_account', args=[1])
        self.assertEqual(resolve(url).func, views.job_seeker_create_account)

    def test_success_page_url(self):
        url = reverse('success_page')
        self.assertEqual(resolve(url).func, views.success_page)

    def test_recruiter_create_account_url(self):
        url = reverse('recruiter_create_account', args=[1])
        self.assertEqual(resolve(url).func, views.recruiter_create_account)

    def test_recruiter_success_page_url(self):
        url = reverse('recruiter_success_page')
        self.assertEqual(resolve(url).func, views.recruiter_success_page)

    def test_recruiter_view_profile_url(self):
        url = reverse('recruiter_view_profile')
        self.assertEqual(resolve(url).func, views.recruiter_view_profile)

    def test_view_jobseeker_profile_by_recruiter_url(self):
        url = reverse('view_jobseeker_profile_by_recruiter', args=[1])
        self.assertEqual(resolve(url).func, views.view_jobseeker_profile_by_recruiter)

    def test_get_report_data_url(self):
        url = reverse('get_report_data')
        self.assertEqual(resolve(url).func, views.get_report_data)

    def test_jobseeker_view_profile_url(self):
        url = reverse('jobseeker_view_profile')
        self.assertEqual(resolve(url).func, views.jobseeker_view_profile)

    def test_view_recruiter_profile_by_jobseeker_url(self):
        url = reverse('view_recruiter_profile_by_jobseeker', args=[1])
        self.assertEqual(resolve(url).func, views.view_recruiter_profile_by_jobseeker)

    def test_quiz_start_screen_url(self):
        url = reverse('quiz_start_screen')
        self.assertEqual(resolve(url).func, views.quiz_start_screen)

    def test_disc_quiz_start_url(self):
        url = reverse('disc_quiz_start')
        self.assertEqual(resolve(url).func, views.disc_quiz_start)

    def test_disc_quiz_url(self):
        url = reverse('disc_quiz', args=['test_question_id'])
        self.assertEqual(resolve(url).func, views.disc_quiz)

    def test_disc_quiz_start_redirect_url(self):
        url = reverse('disc_quiz_start_redirect')
        self.assertEqual(resolve(url).func, views.disc_quiz_start_redirect)

    def test_phase_one_completed_url(self):
        url = reverse('phase_one_completed')
        self.assertEqual(resolve(url).func, views.phase_one_completed)

    def test_disc_completion_url(self):
        url = reverse('disc_completion')
        self.assertEqual(resolve(url).func, views.disc_completion)

    def test_big_five_quiz_start_url(self):
        url = reverse('big_five_quiz_start')
        self.assertEqual(resolve(url).func, views.big_five_quiz_start)

    def test_big_five_quiz_url(self):
        url = reverse('big_five_quiz', args=['test_question_id'])
        self.assertEqual(resolve(url).func, views.big_five_quiz)

    def test_big_five_quiz_start_redirect_url(self):
        url = reverse('big_five_quiz_start_redirect')
        self.assertEqual(resolve(url).func, views.big_five_quiz_start_redirect)

    def test_big_five_completion_url(self):
        url = reverse('big_five_completion')
        self.assertEqual(resolve(url).func, views.big_five_completion)

    def test_non_verbal_quiz_start_url(self):
        url = reverse('non_verbal_quiz_start')
        self.assertEqual(resolve(url).func, views.non_verbal_quiz_start)

    def test_non_verbal_quiz_url(self):
        url = reverse('non_verbal_quiz', args=[1])
        self.assertEqual(resolve(url).func, views.non_verbal_quiz)

    def test_non_verbal_quiz_start_redirect_url(self):
        url = reverse('non_verbal_quiz_start_redirect')
        self.assertEqual(resolve(url).func, views.non_verbal_quiz_start_redirect)

    def test_phase_two_completed_url(self):
        url = reverse('phase_two_completed')
        self.assertEqual(resolve(url).func, views.phase_two_completed)

    def test_non_verbal_completion_url(self):
        url = reverse('non_verbal_completion')
        self.assertEqual(resolve(url).func, views.non_verbal_completion)

    def test_verbal_quiz_start_url(self):
        url = reverse('verbal_quiz_start')
        self.assertEqual(resolve(url).func, views.verbal_quiz_start)

    def test_verbal_quiz_url(self):
        url = reverse('verbal_quiz', args=[1])
        self.assertEqual(resolve(url).func, views.verbal_quiz)

    def test_verbal_quiz_start_redirect_url(self):
        url = reverse('verbal_quiz_start_redirect')
        self.assertEqual(resolve(url).func, views.verbal_quiz_start_redirect)

    def test_verbal_quiz_completion_url(self):
        url = reverse('verbal_quiz_completion')
        self.assertEqual(resolve(url).func, views.verbal_quiz_completion)

    def test_technical_quiz_start_url(self):
        url = reverse('technical_quiz_start')
        self.assertEqual(resolve(url).func, views.technical_quiz_start)

    def test_technical_quiz_url(self):
        url = reverse('technical_quiz', args=[1])
        self.assertEqual(resolve(url).func, views.technical_quiz)

    def test_technical_quiz_start_redirect_url(self):
        url = reverse('technical_quiz_start_redirect')
        self.assertEqual(resolve(url).func, views.technical_quiz_start_redirect)

    def test_phase_three_completed_url(self):
        url = reverse('phase_three_completed')
        self.assertEqual(resolve(url).func, views.phase_three_completed)

    def test_technical_quiz_completion_url(self):
        url = reverse('technical_quiz_completion')
        self.assertEqual(resolve(url).func, views.technical_quiz_completion)

    def test_process_assessment_url(self):
        url = reverse('process_assessment_and_generate_summary')
        self.assertEqual(resolve(url).func, views.process_assessment_and_generate_summary)

    def test_job_seeker_report_url(self):
        url = reverse('job_seeker_report')
        self.assertEqual(resolve(url).func, views.job_seeker_report)

    def test_go_home_jobseeker_url(self):
        url = reverse('go_home_jobseeker')
        self.assertEqual(resolve(url).func, views.go_home_jobseeker)
