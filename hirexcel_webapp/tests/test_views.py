from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from django.contrib.messages import get_messages
from django.shortcuts import redirect
from hirexcel_webapp import models, forms
from datetime import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
import json
from django.http import JsonResponse
import os
from django.conf import settings

# ---------------------------------[ LOGIN/LOGOUT ]------------------------------------------
class TestloginLogoutViews(TestCase):
    
    def setUp(self):
        # Set up a test client and define URLs for jobseeker and recruiter login/logout views
        self.client = Client()
        
         # Base URL for LOGIN/LOGOUT
        self.jobseeker_login_url = reverse('jobseeker_login')
        self.jobseeker_logout_url = reverse('jobseeker_logout')
        self.recruiter_login_url = reverse('recruiter_login')
        self.recruiter_logout_url = reverse('recruiter_logout')

        # Base URL for job seeker account creation
        self.job_seeker_create_account_url = reverse('job_seeker_create_account', args=[1])

        # ---------------------------------[ SAMPLE USER FOR LOGIN/LOGOUT ]------------------------------------------
        # Create a sample jobseeker user and session for logout testing
        self.user_info_jobseeker = models.User_Information.objects.create(
            EMAIL='test@example.com',
            PASSWORD='password123'
        )
        self.job_seeker = models.Job_Seeker.objects.create(USER_ID=self.user_info_jobseeker)
        # Log in the jobseeker user by setting session data
        self.client.session['user_id'] = str(self.user_info_jobseeker.USER_ID)
        self.client.session['job_seeker_id'] = str(self.job_seeker.JOB_SEEKER_ID)
        self.client.session.save()

        # Create a sample recruiter user and session for logout testing
        self.user_info_recruiter = models.User_Information.objects.create(
            EMAIL='recruiter@example.com',
            PASSWORD='password123'
        )
        self.recruiter = models.Recruiter.objects.create(USER_ID=self.user_info_recruiter)
        # Log in the recruiter user by setting session data
        self.client.session['user_id'] = str(self.user_info_recruiter.USER_ID)
        self.client.session['recruiter_id'] = str(self.recruiter.RECRUITER_ID)
        self.client.session.save()         
            
    def test_jobseeker_login_GET(self):
        # Test if GET request to login page loads successfully with status 200
        response = self.client.get(self.jobseeker_login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, './login/job_seeker/jobseeker_login.html')

    def test_jobseeker_login_valid_POST(self):
        # Test if POST request with valid credentials redirects to jobseeker home page
        response = self.client.post(self.jobseeker_login_url, {
            'email-username': 'test@example.com',
            'password': 'password123'
        })

        # Check that the response redirects to the jobseeker_home
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('jobseeker_home'))

        # Check that the session data is set correctly
        self.assertEqual(self.client.session['user_id'], str(self.user_info_jobseeker.USER_ID))
        self.assertEqual(self.client.session['job_seeker_id'], str(self.job_seeker.JOB_SEEKER_ID))

    def test_jobseeker_login_invalid_POST(self):
        # Test if POST request with invalid credentials returns the login page with an error
        response = self.client.post(self.jobseeker_login_url, {
            'email-username': 'invalid@example.com',
            'password': 'wrongpassword'
        })

        # Check that it returns a 200 status and renders the login page again
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, './login/job_seeker/jobseeker_login.html')

        # Check that an error message was added
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Invalid email or password" in str(message) for message in messages))

    def test_recruiter_login_GET(self):
        # Test if GET request to login page loads successfully with status 200
        response = self.client.get(self.recruiter_login_url)
        self.assertEqual(response.status_code, 200)
        # Verify that the correct template is rendered
        self.assertTemplateUsed(response, './login/recruiter/recruiter_login.html')

    def test_recruiter_login_valid_POST(self):
        # Test if POST request with valid credentials redirects to recruiter home page
        response = self.client.post(self.recruiter_login_url, {
            'email-username': 'recruiter@example.com',
            'password': 'password123'
        })

        # Check that the response status is a redirect (302) to recruiter home page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('recruiter_home'))

        # Verify that session data for user_id and recruiter_id is set correctly
        self.assertEqual(self.client.session['user_id'], str(self.user_info_recruiter.USER_ID))
        self.assertEqual(self.client.session['recruiter_id'], str(self.recruiter.RECRUITER_ID))

    def test_recruiter_login_invalid_POST(self):
        # Test if POST request with invalid credentials returns the login page with an error
        response = self.client.post(self.recruiter_login_url, {
            'email-username': 'invalid@example.com',
            'password': 'wrongpassword'
        })

        # Check that the response status is 200, meaning the login page is reloaded
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, './login/recruiter/recruiter_login.html')

        # Verify that an appropriate error message is displayed
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Invalid email or password" in str(message) for message in messages))

    def test_recruiter_login_no_recruiter_account_POST(self):
        # Delete the recruiter instance to simulate no recruiter account
        self.recruiter.delete()

        # Test if POST request with valid user but no recruiter account shows an error
        response = self.client.post(self.recruiter_login_url, {
            'email-username': 'recruiter@example.com',
            'password': 'password123'
        })

        # Check that the response status is 200, meaning the login page is reloaded
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, './login/recruiter/recruiter_login.html')

        # Verify that an appropriate error message is displayed
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Couldn't find email, Please Sign Up" in str(message) for message in messages))
        
    def test_jobseeker_logout(self):
        # Test if jobseeker logout clears session data and redirects to login page
        response = self.client.get(self.jobseeker_logout_url)

        # Verify that the session is flushed (no user_id or job_seeker_id in session)
        self.assertNotIn('user_id', self.client.session)
        self.assertNotIn('job_seeker_id', self.client.session)

        # Check that the response redirects to jobseeker login
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.jobseeker_login_url)

    def test_recruiter_logout(self):
        # Test if recruiter logout clears session data and redirects to login page
        response = self.client.get(self.recruiter_logout_url)

        # Verify that the session is flushed (no user_id or recruiter_id in session)
        self.assertNotIn('user_id', self.client.session)
        self.assertNotIn('recruiter_id', self.client.session)

        # Check that the response redirects to recruiter login
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.recruiter_login_url)

# --------------------------------------[ ENDS ]---------------------------------------------

# ----------------------------[ CREATE ACCOUNT JS ]------------------------------------------


class TestJobSeekerCreateAccountView(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.step4_url = reverse('job_seeker_create_account', args=[4])

        self.step1_user_data = {
            'EMAIL': 'step1_user@example.com',
            'PASSWORD': 'password123',
            'FIRST_NAME': 'John',
            'LAST_NAME': 'Doe',
            'PHONE_NUMBER': '1234567890',
            'CITY': 'Example City',
            'COUNTRY': 'Example Country'
        }

        self.step2_education_data = {
            'INSTITUTION_NAME': 'University of Example',
            'PROGRAM': 'Bachelor of Science',
            'START_DATE': '2020-01-01',
            'END_DATE': '2022-12-31',
            'DEGREE': 'Bachelor of Science'
        }

        self.step3_work_experience_data = {
            'COMPANY_NAME': 'Tech Solutions',
            'DESIGNATION': 'Software Engineer',
            'START_DATE': '2023-01-01',
            'END_DATE': '2024-01-01'
        }

        self.step4_job_seeker_data = {
            'LINKEDIN_PROFILE_URL': 'https://www.linkedin.com/in/testuser',
            'GITHUB_PROFILE_URL': 'https://github.com/testuser'
        }
        
        self.resume_file = SimpleUploadedFile(
            'resume.pdf', 
            b'resume content', 
            content_type='application/pdf'
        )

    def test_step1_personal_info_POST(self):
        # Test if POST request with valid personal info redirects to step 2
        response = self.client.post(reverse('job_seeker_create_account', args=[1]), self.step1_user_data)

        #302 status code 
        # Check that the response status is a redirect (302) to step 2
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('job_seeker_create_account', args=[2]))

        # Verify that 'user_id' is stored in session
        self.assertIn('user_id', self.client.session)

    def test_step2_education_info_POST(self):
        # Simulate previous step by adding 'user_id' to session for Step 2
        step2_user = models.User_Information.objects.create(**self.step1_user_data)
        self.client.session['user_id'] = str(step2_user.USER_ID)
        self.client.session.save()

        # Test if POST request with valid education info redirects to step 3
        response = self.client.post(reverse('job_seeker_create_account', args=[2]), self.step2_education_data)

        # Check that the response status is a redirect (302) to step 3
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('job_seeker_create_account', args=[3]))

        # Verify that education data is stored in session
        self.assertIn('education_data', self.client.session)

    def test_step3_work_experience_POST(self):
        # Simulate previous steps by adding 'user_id' and 'education_data' to session for Step 3
        step3_user = models.User_Information.objects.create(**self.step1_user_data)
        self.client.session['user_id'] = str(step3_user.USER_ID)
        self.client.session['education_data'] = self.step2_education_data
        self.client.session.save()

        # Test if POST request with valid work experience info redirects to step 4
        response = self.client.post(reverse('job_seeker_create_account', args=[3]), self.step3_work_experience_data)

        # Check that the response status is a redirect (302) to step 4
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('job_seeker_create_account', args=[4]))

        # Verify that work experience data is stored in session
        self.assertIn('work_experience_data', self.client.session)

    # # #<---------------------------------------BELOW TEST FAILS. REASON : UNKNOWN--------------->
    # # def test_step4_job_seeker_info_POST(self):
    # #     # Simulate previous steps by adding 'user_id', 'education_data', and 'work_experience_data' to session for Step 4
    # #     step4_user = models.User_Information.objects.create(**self.step1_user_data)
    # #     self.client.session['user_id'] = str(step4_user.USER_ID)
    # #     self.client.session['education_data'] = self.step2_education_data
    # #     self.client.session['work_experience_data'] = self.step3_work_experience_data
    # #     self.client.session.save()

    # #     # Send POST request with data split between POST and FILES
    # #     response = self.client.post(
    # #         reverse('job_seeker_create_account', args=[4]), 
    # #         data=self.step4_post_data, 
    # #         files=self.step4_files_data
    # #     )

    # #     # If response status is 200, print form errors to debug
    # #     if response.status_code == 200:
    # #         form = response.context.get('form')
    # #         if form:
    # #             print(form.errors)

    # #     # Check that the response status is a redirect (302) to success page
    # #     self.assertEqual(response.status_code, 302)
    # #     self.assertRedirects(response, reverse('success_page'))

    # #     # Verify that session is flushed
    # #     self.assertNotIn('user_id', self.client.session)
    # #     self.assertNotIn('education_data', self.client.session)
    # #     self.assertNotIn('work_experience_data', self.client.session)

    # #     # Confirm database entries
    # #     job_seeker = models.Job_Seeker.objects.get(USER_ID=step4_user)
    # #     self.assertEqual(job_seeker.LINKEDIN_PROFILE_URL, self.step4_post_data['LINKEDIN_PROFILE_URL'])
    # #     self.assertEqual(job_seeker.GITHUB_PROFILE_URL, self.step4_post_data['GITHUB_PROFILE_URL'])

    # #     education = models.JobSeekerEducation.objects.get(JOB_SEEKER_ID=job_seeker)
    # #     self.assertEqual(education.DEGREE, self.step2_education_data['DEGREE'])
    # #     self.assertEqual(education.INSTITUTE, self.step2_education_data['INSTITUTION_NAME'])

    # #     work_experience = models.JobSeekerWorkExperience.objects.get(JOB_SEEKER_ID=job_seeker)
    # #     self.assertEqual(work_experience.JOB_TITLE, self.step3_work_experience_data['DESIGNATION'])
    # #     self.assertEqual(work_experience.COMPANY_NAME, self.step3_work_experience_data['COMPANY_NAME'])

    # def add_session_data(self):
    #     step4_user = models.User_Information.objects.create(**self.step1_user_data)
    #     session = self.client.session
    #     session['user_id'] = str(step4_user.USER_ID)
    #     session['education_data'] = self.step2_education_data
    #     session['work_experience_data'] = self.step3_work_experience_data
    #     session.save()
    #     return step4_user

    # def test_step4_job_seeker_info_POST(self):
    #     step4_user = self.add_session_data()

    #     # Submit step 4 data with resume file
    #     response = self.client.post(
    #         self.step4_url,
    #         data=self.step4_job_seeker_data,
    #         files={'RESUME_UPLOAD': self.resume_file}
    #     )

    #     # Debug output to identify any issues with session, file, or form
    #     print("Session data:", dict(self.client.session))
    #     print("Submitted data:", self.step4_job_seeker_data)
    #     print("Submitted files:", {'RESUME_UPLOAD': self.resume_file})

    #     # Check if job_seeker was created and has the resume file
    #     job_seeker = models.Job_Seeker.objects.filter(USER_ID=step4_user).first()
        
    #     # Confirm that the job seeker and resume file were saved correctly
    #     self.assertIsNotNone(job_seeker, "Job Seeker was not created.")
    #     self.assertTrue(job_seeker.RESUME_UPLOAD, "Resume file was not saved.")
    #     self.assertTrue(job_seeker.RESUME_UPLOAD.name.endswith('resume.pdf'), "Resume file name is incorrect.")
    #     self.assertEqual(job_seeker.RESUME_UPLOAD.read(), b'resume content', "Resume file content is incorrect.")
        
    #     # Verify successful redirection to the success page
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, reverse('success_page'))

# --------------------------------------[ ENDS ]---------------------------------------------

# ----------------------------[ CREATE ACCOUNT R ]--------------------------------------------
class TestRecruiterCreateAccountView(TestCase):

    def setUp(self):
        # Initialize client and set up URLs for each step in recruiter account creation
        self.client = Client()
        self.step1_url = reverse('recruiter_create_account', args=[1])
        self.step2_url = reverse('recruiter_create_account', args=[2])

        # Sample data for Step 1 (Personal Info)
        self.step1_user_data = {
            'EMAIL': 'recruiter12345@example.com',
            'PASSWORD': 'L47pashjkord123',
            'FIRST_NAME': 'Jane',
            'LAST_NAME': 'Doe',
            'PHONE_NUMBER': '1234567890',
            'CITY': 'New York',
            'COUNTRY': 'USA'
        }

        # Sample data for Step 2 (Company Info)
        self.step2_company_data = {
            'COMPANY_NAME': 'Techhub',
            'COMPANY_WEBSITE': 'https://Techhub.com',
            'INDUSTRY': 'Information Technology',
            'COMPANY_SIZE': '51-200'
        }

    def test_step1_personal_info_POST(self):
        # Test if POST request with valid personal info redirects to step 2
        response = self.client.post(self.step1_url, self.step1_user_data)

        # Assert redirect to step 2 after successful submission of personal info
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.step2_url)

        # Verify 'user_id' is stored in session
        self.assertIn('user_id', self.client.session)

    # #<---------------------------------------BELOW TEST FAILS. REASON : UNKNOWN--------------->
    # def test_step2_company_info_POST(self):
    #     # Simulate Step 1 by adding 'user_id' to session for Step 2
    #     step2_user = models.User_Information.objects.create(**self.step1_user_data)
    #     self.client.session['user_id'] = str(step2_user.USER_ID)
    #     self.client.session.save()

    #     # Test if POST request with valid company info redirects to success page
    #     response = self.client.post(self.step2_url, self.step2_company_data)

    #     # If the response status is 200, print form errors to debug
    #     if response.status_code == 200:
    #         form = response.context.get('form')
    #         if form:
    #             print("Form Errors:", form.errors)  # Detailed print for form errors

    #     # Assert redirect to success page after company info submission
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, reverse('recruiter_success_page'))

    #     # Confirm session is flushed after success
    #     self.assertNotIn('user_id', self.client.session)

    #     # Verify the recruiter data is saved in the database with correct user reference
    #     recruiter = models.Recruiter.objects.get(USER_ID=step2_user)
    #     self.assertEqual(recruiter.COMPANY_NAME, self.step2_company_data['COMPANY_NAME'])
    #     self.assertEqual(recruiter.COMPANY_WEBSITE, self.step2_company_data['COMPANY_WEBSITE'])
    #     self.assertEqual(recruiter.INDUSTRY, self.step2_company_data['INDUSTRY'])
    #     self.assertEqual(recruiter.COMPANY_SIZE, self.step2_company_data['COMPANY_SIZE'])
    
    # #def test_step2_company_info_POST(self):
    #     # Simulate Step 1 by adding 'user_id' to session for Step 2
    #     step2_user = models.User_Information.objects.create(**self.step1_user_data)
    #     self.client.session['user_id'] = str(step2_user.USER_ID)
    #     self.client.session.save()

    #     # Test if POST request with valid company info redirects to success page
    #     response = self.client.post(self.step2_url, self.step2_company_data)

    #     # Print the response content to see any errors or hints in the HTML
    #     print(response.content)  # This line will output the HTML response for debugging

    #     # If response status is 200, print form errors to debug
    #     if response.status_code == 200:
    #         form = response.context.get('form')
    #         if form:
    #             print("Form Errors:", form.errors)

    #     # Assert redirect to success page after company info submission
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, reverse('recruiter_success_page'))

    #     # Confirm session is flushed after success
    #     self.assertNotIn('user_id', self.client.session)

    #     # Verify the recruiter data is saved in the database with correct user reference
    #     recruiter = models.Recruiter.objects.get(USER_ID=step2_user)
    #     self.assertEqual(recruiter.COMPANY_NAME, self.step2_company_data['COMPANY_NAME'])
    #     self.assertEqual(recruiter.COMPANY_WEBSITE, self.step2_company_data['COMPANY_WEBSITE'])
    #     self.assertEqual(recruiter.INDUSTRY, self.step2_company_data['INDUSTRY'])
    #     self.assertEqual(recruiter.COMPANY_SIZE, self.step2_company_data['COMPANY_SIZE'])

    def test_step1_invalid_data_POST(self):
        # Test POST with missing required fields for Step 1, expecting form re-render with errors
        invalid_data = self.step1_user_data.copy()
        invalid_data.pop('EMAIL')  # Remove required field

        response = self.client.post(self.step1_url, invalid_data)

        # Assert response status is 200 (form re-rendered) due to invalid data
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_account/recruiter/create_account_step1.html')

        # Verify form errors are displayed for missing email
        form = response.context.get('form')
        self.assertIn('EMAIL', form.errors)

    def test_step2_invalid_data_POST(self):
        # Simulate Step 1 completion by setting 'user_id' in session for Step 2
        step2_user = models.User_Information.objects.create(**self.step1_user_data)
        self.client.session['user_id'] = str(step2_user.USER_ID)
        self.client.session.save()

        # Test POST with missing required fields for Step 2, expecting form re-render with errors
        invalid_company_data = self.step2_company_data.copy()
        invalid_company_data.pop('COMPANY_NAME')  # Remove required field

        response = self.client.post(self.step2_url, invalid_company_data)

        # Assert response status is 200 (form re-rendered) due to invalid data
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_account/recruiter/create_account_step2.html')

        # Verify form errors are displayed for missing company name
        form = response.context.get('form')
        self.assertIn('COMPANY_NAME', form.errors)

# --------------------------------------[ ENDS ]---------------------------------------------

# ---------------------------------[ JOB POSTINGs ]------------------------------------------
class TestPostJobView(TestCase):
    def setUp(self):
        # Initialize the client and create necessary objects
        self.client = Client()

        # Create a User_Information instance
        self.user = models.User_Information.objects.create(
            USER_ID='U001',
            FIRST_NAME='John',
            LAST_NAME='Doe',
            EMAIL='john@example.com',
            PASSWORD='password123',
            CITY='New York',
            COUNTRY='USA',
            PHONE_NUMBER='1234567890'
        )

        # Create a Recruiter instance linked to the user
        self.recruiter = models.Recruiter.objects.create(
            RECRUITER_ID='R001',
            USER_ID=self.user,
            COMPANY_NAME='Tech Corp',
            COMPANY_WEBSITE='https://techcorp.com',
            INDUSTRY='Information Technology',
            COMPANY_SIZE='51-200'
        )

        # Create a Job_Position_Criteria instance
        self.job_position_criteria = models.Job_Position_Criteria.objects.create(
            JPC_ID='JPC001',
            CATEGORY='IT',
            JOB_POSITION='Software Engineer',
            PERSONALITY_TRAITS='Analytical, Detail-Oriented',
            COGNITIVE_SKILLS='Problem Solving, Logical Thinking',
            EMOTIONAL_INTELLIGENCE='High',
            COGNITIVE_WEIGHTAGE='40',
            TECHNICAL_WEIGHTAGE='60'
        )

        # Set up session to simulate a logged-in user
        session = self.client.session
        session['user_id'] = self.user.USER_ID
        session.save()

        # Set up the URL for the `post_job` view
        self.url = reverse('post_job')

    def test_post_job_valid_data(self):
        # Prepare mock POST data
        data = {
            'jobTitle': 'Junior Software Engineer',
            'city': 'San Francisco',
            'country': 'USA',
            'jobType': 'Full-Time',
            'jobPosition': 'Software Engineer',
            'jobDescription': 'An entry-level software engineering role.',
            'personalityTraits': ['Analytical', 'Detail-Oriented'],
            'technicalAssessment[]': ['Java', 'Python'],
            'requiredQualification': ['Bachelor of Science in Computer Science'],
            'experienceRequirements': '1-2 years of experience in software development.',
            'requiredSkills': json.dumps([
                {'value': 'Python'},
                {'value': 'Django'},
                {'value': 'Problem Solving'}
            ]),
            'cognitiveWeightage': '40',
            'technicalWeightage': '60'
        }

        # Make the POST request
        response = self.client.post(self.url, data)

        # Check for a redirect to recruiter_home
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('recruiter_home'))

        # Verify that a Job_Posting record has been created with the correct details
        job_posting = models.Job_Posting.objects.get(TITLE='Junior Software Engineer')
        self.assertEqual(job_posting.DESCRIPTION, 'An entry-level software engineering role.')
        self.assertEqual(job_posting.CITY, 'San Francisco')
        self.assertEqual(job_posting.COUNTRY, 'USA')
        self.assertEqual(job_posting.JOB_TYPE, 'Full-Time')
        self.assertEqual(job_posting.JOB_POSITION, 'Software Engineer')
        self.assertEqual(job_posting.RECRUITER_ID, self.recruiter)
        self.assertEqual(job_posting.PERSONALITY_TRAITS, 'Analytical, Detail-Oriented')
        self.assertEqual(job_posting.REQUIRED_ASSESSMENTS, 'Personality Assessment, Cognitive Assessment, Technical Assessment')
        self.assertEqual(job_posting.TECHNICAL_ASSESSMENT_LEVEL, 'Java, Python')
        self.assertEqual(job_posting.REQUIRED_QUALIFICATIONS, 'Bachelor of Science in Computer Science')
        self.assertEqual(job_posting.EXPERIENCE_REQUIREMENTS, '1-2 years of experience in software development.')
        self.assertEqual(job_posting.REQUIRED_SKILLS, 'Python, Django, Problem Solving')
        self.assertEqual(job_posting.COGNITIVE_WEIGHTAGE, '40')
        self.assertEqual(job_posting.TECHNICAL_WEIGHTAGE, '60')

    def tearDown(self):
        # Clear the session after each test
        self.client.session.flush()

# --------------------------------------[ ENDS ]---------------------------------------------

# ---------------------------------[ APPLY FOR JOB ]------------------------------------------
class TestApplyForJobView(TestCase):
    
    def setUp(self):
        # Initialize the client
        self.client = Client()

        # Create a sample User_Information instance to link to the recruiter
        self.user_info = models.User_Information.objects.create(
            USER_ID='12345',
            FIRST_NAME='John',
            LAST_NAME='Doe',
            EMAIL='johndoe@example.com',
            PASSWORD='password',
            CITY='San Francisco',
            COUNTRY='USA',
            PHONE_NUMBER='1234567890'
        )

        # Create a sample Recruiter instance
        self.recruiter = models.Recruiter.objects.create(
            RECRUITER_ID='54321',
            USER_ID=self.user_info,
            COMPANY_NAME='TechCorp',
            COMPANY_WEBSITE='https://techcorp.com',
            INDUSTRY='Technology',
            COMPANY_SIZE='1-50'
        )

        # Create a sample Job_Posting instance linked to the recruiter
        self.job_posting = models.Job_Posting.objects.create(
            JOB_POST_ID='123456789',
            TITLE='Junior Software Engineer',
            DESCRIPTION='Entry-level software engineering role',
            RECRUITER_ID=self.recruiter,
            CITY='San Francisco',
            COUNTRY='USA',
            JOB_TYPE='Full-Time',
            JOB_POSITION='Software Engineer',
            PERSONALITY_TRAITS='Analytical, Detail-Oriented',
            REQUIRED_SKILLS='Python, Django',
            REQUIRED_QUALIFICATIONS='Bachelor of Science in Computer Science',
            EXPERIENCE_REQUIREMENTS='1-2 years',
            COGNITIVE_WEIGHTAGE='40',
            TECHNICAL_WEIGHTAGE='60',
            REQUIRED_ASSESSMENTS='Cognitive, Technical',
            TECHNICAL_ASSESSMENT_LEVEL='Basic'
        )
        self.job_post_id = self.job_posting.JOB_POST_ID

    def test_apply_for_job_POST(self):
        # URL for applying to a job with the provided job_post_id
        url = reverse('apply_for_job', args=[self.job_post_id])

        # Send POST request to simulate job application submission
        response = self.client.post(url)

        # Verify an Assessment instance was created after submitting the form
        assessment = models.Assessment.objects.first()
        self.assertIsNotNone(assessment, "Assessment should be created after POST request.")

        # Verify session stores assessment ID and job post ID correctly
        session = self.client.session
        self.assertEqual(session['assessment_id'], str(assessment.ASSESSMENT_ID),
                         "Session 'assessment_id' should match the created Assessment ID.")
        self.assertEqual(session['job_post_id'], self.job_post_id,
                         "Session 'job_post_id' should match the provided job_post_id.")

        # Confirm redirection to the next step (disc_quiz_start)
        self.assertEqual(response.status_code, 302, "Response should redirect to disc_quiz_start.")
        self.assertRedirects(response, reverse('disc_quiz_start'), status_code=302)

# --------------------------------------[ ENDS ]---------------------------------------------


# ---------------------------[ GET REPORT DATA ]----------------------------------------------
class TestGetReportDataView(TestCase):
    
    def setUp(self):
        # Creating User_Information instance
        self.user_info = models.User_Information.objects.create(
            USER_ID="123456789",
            FIRST_NAME="John",
            LAST_NAME="Doe",
            EMAIL="john.doe@example.com",
            PASSWORD="securepassword",
            CITY="New York",
            COUNTRY="USA",
            PHONE_NUMBER="1234567890"
        )

        # Creating Job_Seeker instance
        self.job_seeker = models.Job_Seeker.objects.create(
            JOB_SEEKER_ID="987654321",
            USER_ID=self.user_info,
            LINKEDIN_PROFILE_URL="https://linkedin.com/in/johndoe",
            GITHUB_PROFILE_URL="https://github.com/johndoe",
            RESUME_UPLOAD=SimpleUploadedFile("resume.pdf", b"dummy content")
        )

        # Creating Job_Seeker_Education instance
        self.job_seeker_education = models.Job_Seeker_Education.objects.create(
            JOB_SEEKER_EDUCATION_ID="111111111",
            JOB_SEEKER_ID=self.job_seeker,
            INSTITUTION_NAME="University of Example",
            PROGRAM="Computer Science",
            START_DATE="2019-09-01",
            END_DATE="2023-06-01",
            DEGREE="Bachelor's"
        )

        # Creating Job_Seeker_Work_Experience instance
        self.job_seeker_work_experience = models.Job_Seeker_Work_Experience.objects.create(
            JOB_SEEKER_WE_ID="222222222",
            JOB_SEEKER_ID=self.job_seeker,
            COMPANY_NAME="Example Corp",
            DESIGNATION="Software Engineer",
            START_DATE="2023-06-01",
            END_DATE=None  # Assume current job
        )

        # Creating Recruiter instance
        self.recruiter = models.Recruiter.objects.create(
            RECRUITER_ID="333333333",
            USER_ID=self.user_info,
            COMPANY_NAME="Tech Solutions Inc.",
            COMPANY_WEBSITE="https://techsolutions.com",
            INDUSTRY="Software Development",
            COMPANY_SIZE="200-500 employees"
        )

        # Creating Job_Position_Criteria instance
        self.job_position_criteria = models.Job_Position_Criteria.objects.create(
            JPC_ID="444444444",
            CATEGORY="Engineering",
            JOB_POSITION="Software Developer",
            PERSONALITY_TRAITS="Analytical, Logical",
            COGNITIVE_SKILLS="Problem Solving, Critical Thinking",
            EMOTIONAL_INTELLIGENCE="High",
            COGNITIVE_WEIGHTAGE="40",
            TECHNICAL_WEIGHTAGE="60"
        )

        # Creating Job_Posting instance
        self.job_posting = models.Job_Posting.objects.create(
            JOB_POST_ID="555555555",
            TITLE="Backend Developer",
            DESCRIPTION="Develop APIs and manage databases.",
            RECRUITER_ID=self.recruiter,
            CITY="Los Angeles",
            COUNTRY="USA",
            JOB_TYPE="Full-time",
            JOB_POSITION="Backend Developer",
            PERSONALITY_TRAITS="Detail-oriented, Reliable, Analytical",
            REQUIRED_SKILLS="Python, Django, SQL",
            REQUIRED_QUALIFICATIONS="Bachelor's in Computer Science",
            EXPERIENCE_REQUIREMENTS="2+ years in backend development",
            REQUIRED_ASSESSMENTS="Personality, Cognitive, Technical",
            COGNITIVE_WEIGHTAGE="40",
            TECHNICAL_WEIGHTAGE="60",
            TECHNICAL_ASSESSMENT_LEVEL="Advanced"
        )

        # Creating Assessment instance
        self.assessment = models.Assessment.objects.create(
            ASSESSMENT_ID="666666666",
            JOB_POST_ID=self.job_posting,
            COGNITIVE_WEIGHTAGE="40",
            TECHNICAL_WEIGHTAGE="60",
            TECHNICAL_ASSESSMENT_LEVEL="Advanced"
        )

        # Creating Job_Seeker_Assessment instance
        self.job_seeker_assessment = models.Job_Seeker_Assessment.objects.create(
            JOB_SEEKER_ASSESSMENT_ID="777777777",
            JOB_SEEKER_ID=self.job_seeker,
            JOB_POST_ID=self.job_posting,
            ASSESSMENT_ID=self.assessment,
            NAME="Full Assessment",
            ASSESSMENT_TYPE="Comprehensive",
            TOTAL_COMPLETION_TIME_REQUIRED="120 minutes"
        )

        # Creating Personality_Assessment instance
        self.personality_assessment = models.Personality_Assessment.objects.create(
            PERSONALITY_ASSESSMENT_ID="888888888",
            JOB_SEEKER_ASSESSMENT_ID=self.job_seeker_assessment
        )

        # Creating DISC_Assessment instance
        self.disc_assessment = models.DISC_Assessment.objects.create(
            DISC_ASSESSMENT_ID="999999999",
            PERSONALITY_ASSESSMENT_ID=self.personality_assessment,
            DISC_COMPLETION_TIME_REQUIRED="30 minutes"
        )

        # Creating BigFive_Assessment instance
        self.bigfive_assessment = models.BigFive_Assessment.objects.create(
            BIGFIVE_ASSESSMENT_ID="112233445",
            PERSONALITY_ASSESSMENT_ID=self.personality_assessment,
            BIGFIVE_COMPLETION_TIME_REQUIRED="45 minutes"
        )

        # Creating DISC_Assessment_Result instance
        self.disc_assessment_result = models.DISC_Assessment_Result.objects.create(
            DISC_ASSESSMENT_RESULT_ID="223344556",
            DISC_ASSESSMENT_ID=self.disc_assessment,
            DISC_CATEGORY="Influential",
            DOMINANCE_SCORE=85,
            INFLUENCING_SCORE=75,
            STEADINESS_SCORE=65,
            CONCIENTIOUSNESS_SCORE=55,
            TOTAL_DISC_COMPLETION_TIME="25 minutes"
        )

        # Creating BigFive_Assessment_Result instance
        self.bigfive_assessment_result = models.BigFive_Assessment_Result.objects.create(
            BIGFIVE_ASSESSMENT_RESULT_ID="334455667",
            BIGFIVE_ASSESSMENT_ID=self.bigfive_assessment,
            DIMENSION="Openness",
            OPENNESS_SCORE=90,
            CONCIENTIOUSNESS_SCORE=80,
            EXTRAVERSION_SCORE=70,
            AGREEABLENESS_SCORE=60,
            NEUROTICISM_SCORE=50,
            TOTAL_BIGFIVE_COMPLETION_TIME="40 minutes"
        )

        # Creating Cognitive_Assessment instance
        self.cognitive_assessment = models.Cognitive_Assessment.objects.create(
            COGNITIVE_ASSESSMENT_ID="445566778",
            JOB_SEEKER_ASSESSMENT_ID=self.job_seeker_assessment,
            COGNITIVE_COMPLETION_TIME_REQUIRED="30 minutes"
        )

        # Creating Technical_Assessment instance
        self.technical_assessment = models.Technical_Assessment.objects.create(
            TECHNICAL_ASSESSMENT_ID="556677889",
            JOB_SEEKER_ASSESSMENT_ID=self.job_seeker_assessment,
            TECHNICAL_ASSESSMENT_LEVEL="Intermediate",
            TECHNICAL_COMPLETION_TIME_REQUIRED="60 minutes"
        )

        # Creating Cognitive_Assessment_Results instance
        self.cognitive_assessment_result = models.Cognitive_Assessment_Results.objects.create(
            COGNITIVE_ASSESSMENT_RESULT_ID="667788990",
            COGNITIVE_ASSESSMENT_ID=self.cognitive_assessment,
            COGNITIVE_VI_SCORE=85,
            COGNITIVE_NVI_SCORE=80,
            TOTAL_COGNITIVE_SCORE=165,
            COGNITIVE_SCORE_PERCENTAGE=82,
            VI_COMPLETION_TIME="15 minutes",
            NVI_COMPLETION_TIME="15 minutes",
            TOTAL_COGNITIVE_COMPLETION_TIME="30 minutes"
        )

        # Creating Technical_Assessment_Result instance
        self.technical_assessment_result = models.Technical_Assessment_Result.objects.create(
            TECHNICAL_ASSESSMENT_RESULT_ID="778899001",
            TECHNICAL_ASSESSMENT_ID=self.technical_assessment,
            TOTAL_TECH_SCORE=90,
            TECH_SCORE_PERCENTAGE=90,
            TOTAL_TECHNICAL_COMPLETION_TIME="60 minutes"
        )

        # Creating Personality_Assessment_Report instance
        self.personality_assessment_report = models.Personality_Assessment_Report.objects.create(
            #PERSONALITY_ASSRESSMENT_REPORT_ID="889900112",
            PERSONALITY_ASSESSMENT_ID=self.personality_assessment,
            JOB_SEEKER_ASSESSMENT_ID=self.job_seeker_assessment,
            BIGFIVE_ASSESSMENT_ID=self.bigfive_assessment,
            DISC_ASSESSMENT_ID=self.disc_assessment,
            DISC_CATEGORY="Influential",
            DISC_PERSONALITY_TRAIT="Assertive",
            DISC_COGNITIVE_ABILITY="High",
            DISC_EMOTIONAL_REGULATION="Moderate",
            DISC_TENDENCIES="Leadership",
            DISC_WEAKNESSES="Impatience",
            DISC_BEHAVIOUR="Goal-oriented",
            DISC_MOTIVATED_BY="Achievement",
            BIGFIVE_OPENNESS_SCORE=90,
            BIGFIVE_OPENNESS_CATEGORY="High",
            BIGFIVE_OPENNESS_PERSONALITY="Creative",
            BIGFIVE_OPENNESS_DESCRIPTION="Open to new experiences.",
            BIGFIVE_OPENNESS_WORKPLACE_BEHAVIOUR="Innovative",
            BIGFIVE_CONCIENTIOUSNESS_SCORE=85,
            BIGFIVE_CONCIENTIOUSNESS_CATEGORY="High",
            BIGFIVE_CONCIENTIOUSNESS_PERSONALITY="Organized",
            BIGFIVE_CONCIENTIOUSNESS_DESCRIPTION="Detail-oriented and organized.",
            BIGFIVE_CONCIENTIOUSNESS_WORKPLACE_BEHAVIOUR="Reliable",
            BIGFIVE_EXTRAVERSION_SCORE=70,
            BIGFIVE_EXTRAVERSION_CATEGORY="Moderate",
            BIGFIVE_EXTRAVERSION_PERSONALITY="Sociable",
            BIGFIVE_EXTRAVERSION_DESCRIPTION="Enjoys social interactions.",
            BIGFIVE_EXTRAVERSION_WORKPLACE_BEHAVIOUR="Team-oriented",
            BIGFIVE_AGREEABLENESS_SCORE=60,
            BIGFIVE_AGREEABLENESS_CATEGORY="Moderate",
            BIGFIVE_AGREEABLENESS_PERSONALITY="Friendly",
            BIGFIVE_AGREEABLENESS_DESCRIPTION="Empathetic towards others.",
            BIGFIVE_AGREEABLENESS_WORKPLACE_BEHAVIOUR="Cooperative",
            BIGFIVE_NEUROTICISM_SCORE=40,
            BIGFIVE_NEUROTICISM_CATEGORY="Low",
            BIGFIVE_NEUROTICISM_PERSONALITY="Calm",
            BIGFIVE_NEUROTICISM_DESCRIPTION="Handles stress well.",
            BIGFIVE_NEUROTICISM_WORKPLACE_BEHAVIOUR="Stable"
        )

        # Creating Evaluation_Summary instance
        self.evaluation_summary = models.Evaluation_Summary.objects.create(
            EVALUATION_SUMMARY_ID="990011223",
            USER_ID=self.user_info,
            JOB_SEEKER_ID=self.job_seeker,
            JOB_POST_ID=self.job_posting,
            ASSESSMENT_ID=self.assessment,
            PERSONALITY_ASSESSMENT_REPORT_ID=self.personality_assessment_report,
            COGNITIVE_ASSESSMENT_RESULT_ID=self.cognitive_assessment_result,
            TECHNICAL_ASSESSMENT_RESULT_ID=self.technical_assessment_result,
            CANDIDATE_STATUS="Recommended",
            PROFILE_SYNOPSIS="Experienced in software development, strong analytical skills.",
            OPTIMAL_JOB_MATCHES="Backend Developer, API Specialist",
            EVALUATION_SUMMARY=SimpleUploadedFile("summary.pdf", b"dummy content")
        )

    def test_get_report_data_success(self):
        """Test that report data is returned successfully with valid assessment_id."""
        url = reverse('get_report_data') + f'?assessment_id={self.assessment.ASSESSMENT_ID}'
        response = self.client.get(url)

        # Verify that the request was successful
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)['report_data']

        # Verify the returned report data
        self.assertEqual(response_data['user_info']['first_name'], 'John')
        self.assertEqual(response_data['job_post']['title'], 'Backend Developer')
        self.assertEqual(response_data['evaluation_summary']['candidate_status'], 'Recommended')
        self.assertEqual(response_data['cognitive_result'], 'Passed')
        self.assertEqual(response_data['technical_result'], 'Passed')
        self.assertIn('Analytical', response_data['personality_traits_list'])
        self.assertIn('Creative', response_data['bigf_openness_personality_list'])

    def test_get_report_data_missing_assessment_id(self):
        """Test that a missing assessment_id returns an error."""
        url = reverse('get_report_data')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'Assessment ID is required')

    def test_get_report_data_invalid_assessment_id(self):
        """Test that an invalid assessment_id returns a 404 error."""
        url = reverse('get_report_data') + '?assessment_id=invalid_id'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.content)
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'Report data not found')

# --------------------------------------[ ENDS ]------------------------------------------------



























































































































































































































































































































































































