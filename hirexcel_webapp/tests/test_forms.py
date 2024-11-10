from django.test import TestCase
from hirexcel_webapp.forms import (
    LoginForm, UserInformationForm, JobSeekerForm, JobSeekerEducationForm,
    JobSeekerWorkExperienceForm, RecruiterForm, JobPostingForm
)
from django.core.files.uploadedfile import SimpleUploadedFile


class FormsTest(TestCase):

    def test_login_form_valid_data(self):
        """
        Scenario: Valid login form submission with correct email and password format.
        """
        form = LoginForm(data={'email': 'test@example.com', 'password': 'password123'})
        self.assertTrue(form.is_valid())

    def test_login_form_invalid_data(self):
        """
        Scenario: Invalid login form submission with an incorrect email format.
        """
        form = LoginForm(data={'email': 'invalid-email', 'password': 'password123'})
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_user_information_form_valid_data(self):
        """
        Scenario: User information form with all fields correctly populated.
        """
        form = UserInformationForm(data={
            'FIRST_NAME': 'John', 'LAST_NAME': 'Doe', 'EMAIL': 'johndoe@example.com',
            'PASSWORD': 'securepassword', 'CITY': 'New York', 'COUNTRY': 'USA', 'PHONE_NUMBER': '1234567890'
        })
        self.assertTrue(form.is_valid())

    def test_user_information_form_missing_required_fields(self):
        """
        Scenario: User information form submission missing required fields.
        """
        form = UserInformationForm(data={'FIRST_NAME': 'John', 'EMAIL': 'johndoe@example.com'})
        self.assertFalse(form.is_valid())
        self.assertIn('LAST_NAME', form.errors)
        self.assertIn('PASSWORD', form.errors)

    def test_job_seeker_form_valid_data(self):
        """
        Scenario: Job seeker form submission with valid URLs and resume file.
        """
        resume_file = SimpleUploadedFile("resume.pdf", b"Resume content", content_type="application/pdf")
        form = JobSeekerForm(data={
            'LINKEDIN_PROFILE_URL': 'https://linkedin.com/in/johndoe',
            'GITHUB_PROFILE_URL': 'https://github.com/johndoe'
        }, files={'RESUME_UPLOAD': resume_file})
        self.assertTrue(form.is_valid())

    def test_job_seeker_form_invalid_url(self):
        """
        Scenario: Job seeker form submission with incorrectly formatted URLs.
        """
        form = JobSeekerForm(data={
            'LINKEDIN_PROFILE_URL': 'invalid-url', 'GITHUB_PROFILE_URL': 'invalid-url'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('LINKEDIN_PROFILE_URL', form.errors)
        self.assertIn('GITHUB_PROFILE_URL', form.errors)

    def test_job_seeker_education_form_valid_data(self):
        """
        Scenario: Job seeker education form with all fields correctly filled.
        """
        form = JobSeekerEducationForm(data={
            'INSTITUTION_NAME': 'University of Example', 'PROGRAM': 'Bachelor of Science',
            'START_DATE': '2020-01-01', 'END_DATE': '2022-12-31', 'DEGREE': 'B.Sc.'
        })
        self.assertTrue(form.is_valid())

    def test_job_seeker_education_form_missing_fields(self):
        """
        Scenario: Job seeker education form submission with missing required fields.
        """
        form = JobSeekerEducationForm(data={'INSTITUTION_NAME': 'University of Example'})
        self.assertFalse(form.is_valid())
        self.assertIn('START_DATE', form.errors)

    def test_job_seeker_work_experience_form_valid_data(self):
        """
        Scenario: Job seeker work experience form with all fields correctly filled.
        """
        form = JobSeekerWorkExperienceForm(data={
            'COMPANY_NAME': 'Tech Corp', 'DESIGNATION': 'Software Engineer',
            'START_DATE': '2022-01-01', 'END_DATE': '2023-01-01'
        })
        self.assertTrue(form.is_valid())

    def test_job_seeker_work_experience_form_missing_fields(self):
        """
        Scenario: Job seeker work experience form submission with missing required fields.
        """
        form = JobSeekerWorkExperienceForm(data={'COMPANY_NAME': 'Tech Corp'})
        self.assertFalse(form.is_valid())
        self.assertIn('DESIGNATION', form.errors)
        self.assertIn('START_DATE', form.errors)

    def test_recruiter_form_valid_data(self):
        """
        Scenario: Recruiter form submission with valid URLs and populated fields.
        """
        form = RecruiterForm(data={
            'COMPANY_NAME': 'Tech Corp', 'COMPANY_WEBSITE': 'https://techcorp.com',
            'INDUSTRY': 'Software', 'COMPANY_SIZE': '200-500'
        })
        self.assertTrue(form.is_valid())

    def test_recruiter_form_invalid_url(self):
        """
        Scenario: Recruiter form submission with an invalid URL format.
        """
        form = RecruiterForm(data={
            'COMPANY_NAME': 'Tech Corp', 'COMPANY_WEBSITE': 'invalid-url'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('COMPANY_WEBSITE', form.errors)

    def test_job_posting_form_valid_data(self):
        """
        Scenario: Job posting form submission with all fields correctly populated.
        """
        form = JobPostingForm(data={
            'TITLE': 'Software Engineer', 'DESCRIPTION': 'Job description here',
            'CITY': 'New York', 'COUNTRY': 'USA', 'JOB_TYPE': 'Full-Time', 'JOB_POSITION': 'Engineer'
        })
        self.assertTrue(form.is_valid())

    def test_job_posting_form_missing_fields(self):
        """
        Scenario: Job posting form submission missing required fields.
        """
        form = JobPostingForm(data={'TITLE': 'Software Engineer'})
        self.assertFalse(form.is_valid())
        self.assertIn('DESCRIPTION', form.errors)
        self.assertIn('CITY', form.errors)
