from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, ANY
from hirexcel_webapp import models

from django.core.files.uploadedfile import SimpleUploadedFile

class TestProcessAssessmentAndGenerateSummary(TestCase):

    def setUp(self):
        # Setting up test client and view URL
        self.client = Client()
        self.url = reverse('process_assessment_and_generate_summary')

        # Create User Information and Recruiter
        self.user_info = models.User_Information.objects.create(
            USER_ID="123456789", FIRST_NAME="Test", LAST_NAME="User",
            EMAIL="testuser@example.com", PASSWORD="password", PHONE_NUMBER="1234567890",
            CITY="City", COUNTRY="Country"
        )
        self.recruiter = models.Recruiter.objects.create(
            RECRUITER_ID="987654321", USER_ID=self.user_info,
            COMPANY_NAME="Test Company", COMPANY_WEBSITE="https://testcompany.com"
        )

        # Job Seeker with Linked Data
        self.job_seeker = models.Job_Seeker.objects.create(
            JOB_SEEKER_ID="876543210", USER_ID=self.user_info,
            LINKEDIN_PROFILE_URL="https://linkedin.com/in/testuser",
            GITHUB_PROFILE_URL="https://github.com/testuser",
            RESUME_UPLOAD=SimpleUploadedFile('resume.pdf', b'resume content', content_type='application/pdf')
        )
        self.job_seeker_education = models.Job_Seeker_Education.objects.create(
            JOB_SEEKER_EDUCATION_ID="101010101", JOB_SEEKER_ID=self.job_seeker,
            INSTITUTION_NAME="University of Test", PROGRAM="B.Sc Computer Science",
            START_DATE="2015-09-01", END_DATE="2019-06-01", DEGREE="Bachelor's"
        )
        self.job_seeker_work_experience = models.Job_Seeker_Work_Experience.objects.create(
            JOB_SEEKER_WE_ID="202020202", JOB_SEEKER_ID=self.job_seeker,
            COMPANY_NAME="Test Solutions", DESIGNATION="Software Engineer",
            START_DATE="2020-01-01", END_DATE="2023-01-01"
        )

        # Job Posting and Assessment Setup
        self.job_post = models.Job_Posting.objects.create(
            JOB_POST_ID="303030303", TITLE="Software Engineer", RECRUITER_ID=self.recruiter,
            CITY="City", COUNTRY="Country", JOB_TYPE="Full-Time", JOB_POSITION="Developer",
            PERSONALITY_TRAITS="Analytical", REQUIRED_SKILLS="Python",
            REQUIRED_QUALIFICATIONS="Bachelor's Degree", EXPERIENCE_REQUIREMENTS="2 Years",
            REQUIRED_ASSESSMENTS="DISC, BigFive", COGNITIVE_WEIGHTAGE="50",
            TECHNICAL_WEIGHTAGE="50", TECHNICAL_ASSESSMENT_LEVEL="Intermediate"
        )
        self.assessment = models.Assessment.objects.create(
            ASSESSMENT_ID="404040404", JOB_POST_ID=self.job_post,
            COGNITIVE_WEIGHTAGE="50", TECHNICAL_WEIGHTAGE="50",
            TECHNICAL_ASSESSMENT_LEVEL="Intermediate"
        )

        # Job Seeker Assessment, Personality Assessment, and Reports
        self.job_seeker_assessment = models.Job_Seeker_Assessment.objects.create(
            JOB_SEEKER_ASSESSMENT_ID="505050505", JOB_SEEKER_ID=self.job_seeker,
            JOB_POST_ID=self.job_post, ASSESSMENT_ID=self.assessment,
            NAME="DISC Assessment", ASSESSMENT_TYPE="DISC",
            TOTAL_COMPLETION_TIME_REQUIRED="60 minutes"
        )
        self.personality_assessment = models.Personality_Assessment.objects.create(
            PERSONALITY_ASSESSMENT_ID="606060606", JOB_SEEKER_ASSESSMENT_ID=self.job_seeker_assessment
        )
        self.disc_assessment = models.DISC_Assessment.objects.create(
            DISC_ASSESSMENT_ID="707070707", PERSONALITY_ASSESSMENT_ID=self.personality_assessment,
            DISC_COMPLETION_TIME_REQUIRED="30 minutes"
        )
        self.bigfive_assessment = models.BigFive_Assessment.objects.create(
            BIGFIVE_ASSESSMENT_ID="808080808", PERSONALITY_ASSESSMENT_ID=self.personality_assessment,
            BIGFIVE_COMPLETION_TIME_REQUIRED="30 minutes"
        )
        self.personality_assessment_report = models.Personality_Assessment_Report.objects.create(
            PERSONALITY_ASSESSMENT_REPORT_ID="909090909", PERSONALITY_ASSESSMENT_ID=self.personality_assessment,
            JOB_SEEKER_ASSESSMENT_ID=self.job_seeker_assessment, DISC_ASSESSMENT_ID=self.disc_assessment,
            BIGFIVE_ASSESSMENT_ID=self.bigfive_assessment, DISC_CATEGORY="High",
            DISC_PERSONALITY_TRAIT="Analytical", DISC_COGNITIVE_ABILITY="Good",
            DISC_EMOTIONAL_REGULATION="Stable", DISC_TENDENCIES="Team Player",
            DISC_WEAKNESSES="None", DISC_BEHAVIOUR="Collaborative",
            DISC_MOTIVATED_BY="Challenge", BIGFIVE_OPENNESS_SCORE=80,
            BIGFIVE_OPENNESS_CATEGORY="High", BIGFIVE_OPENNESS_PERSONALITY="Curious",
            BIGFIVE_OPENNESS_DESCRIPTION="Open-minded", BIGFIVE_OPENNESS_WORKPLACE_BEHAVIOUR="Creative",
            BIGFIVE_CONCIENTIOUSNESS_SCORE=85, BIGFIVE_CONCIENTIOUSNESS_CATEGORY="High",
            BIGFIVE_CONCIENTIOUSNESS_PERSONALITY="Organized", BIGFIVE_CONCIENTIOUSNESS_DESCRIPTION="Structured",
            BIGFIVE_CONCIENTIOUSNESS_WORKPLACE_BEHAVIOUR="Detail-Oriented", BIGFIVE_EXTRAVERSION_SCORE=70,
            BIGFIVE_EXTRAVERSION_CATEGORY="Moderate", BIGFIVE_EXTRAVERSION_PERSONALITY="Outgoing",
            BIGFIVE_EXTRAVERSION_DESCRIPTION="Friendly", BIGFIVE_EXTRAVERSION_WORKPLACE_BEHAVIOUR="Approachable",
            BIGFIVE_AGREEABLENESS_SCORE=65, BIGFIVE_AGREEABLENESS_CATEGORY="Moderate",
            BIGFIVE_AGREEABLENESS_PERSONALITY="Trusting", BIGFIVE_AGREEABLENESS_DESCRIPTION="Cooperative",
            BIGFIVE_AGREEABLENESS_WORKPLACE_BEHAVIOUR="Team-Oriented", BIGFIVE_NEUROTICISM_SCORE=50,
            BIGFIVE_NEUROTICISM_CATEGORY="Low", BIGFIVE_NEUROTICISM_PERSONALITY="Calm",
            BIGFIVE_NEUROTICISM_DESCRIPTION="Relaxed", BIGFIVE_NEUROTICISM_WORKPLACE_BEHAVIOUR="Stable"
        )

        # Cognitive and Technical Assessment Setup
        self.cognitive_assessment = models.Cognitive_Assessment.objects.create(
            COGNITIVE_ASSESSMENT_ID="1010101010", JOB_SEEKER_ASSESSMENT_ID=self.job_seeker_assessment,
            COGNITIVE_COMPLETION_TIME_REQUIRED="45 minutes"
        )
        self.cognitive_assessment_result = models.Cognitive_Assessment_Results.objects.create(
            COGNITIVE_ASSESSMENT_RESULT_ID="1111111111", COGNITIVE_ASSESSMENT_ID=self.cognitive_assessment,
            COGNITIVE_VI_SCORE=60, COGNITIVE_NVI_SCORE=65, TOTAL_COGNITIVE_SCORE=62,
            COGNITIVE_SCORE_PERCENTAGE=60, VI_COMPLETION_TIME="10m", NVI_COMPLETION_TIME="15m",
            TOTAL_COGNITIVE_COMPLETION_TIME="25m"
        )
        self.technical_assessment = models.Technical_Assessment.objects.create(
            TECHNICAL_ASSESSMENT_ID="1212121212", JOB_SEEKER_ASSESSMENT_ID=self.job_seeker_assessment,
            TECHNICAL_ASSESSMENT_LEVEL="Intermediate", TECHNICAL_COMPLETION_TIME_REQUIRED="30 minutes"
        )
        self.technical_assessment_result = models.Technical_Assessment_Result.objects.create(
            TECHNICAL_ASSESSMENT_RESULT_ID="1313131313", TECHNICAL_ASSESSMENT_ID=self.technical_assessment,
            TOTAL_TECH_SCORE=80, TECH_SCORE_PERCENTAGE=75, TOTAL_TECHNICAL_COMPLETION_TIME="20m"
        )

        # Set up session data
        session = self.client.session
        session['user_id'] = self.user_info.USER_ID
        session['JOB_SEEKER_ID'] = self.job_seeker.JOB_SEEKER_ID
        session['ASSESSMENT_ID'] = self.assessment.ASSESSMENT_ID
        session['PERSONALITY_ASSESSMENT_ID'] = self.personality_assessment.PERSONALITY_ASSESSMENT_ID
        session['COGNITIVE_ASSESSMENT_ID'] = self.cognitive_assessment.COGNITIVE_ASSESSMENT_ID
        session['TECHNICAL_ASSESSMENT_ID'] = self.technical_assessment.TECHNICAL_ASSESSMENT_ID
        session.save()

    # Now you can add your test cases using the above data setup


    @patch('hirexcel_webapp.views.ChatGPTIntegration.generate_candidate_status')
    @patch('hirexcel_webapp.views.ChatGPTIntegration.generate_profile_synopsis')
    @patch('hirexcel_webapp.views.ChatGPTIntegration.generate_optimal_job_matches')
    def test_process_assessment_and_generate_summary(self, mock_optimal_job_matches, mock_profile_synopsis, mock_candidate_status):
        """
        Scenario:
        This test verifies the functionality of the `process_assessment_and_generate_summary` view. 
        It simulates the assessment and summary generation process for a job seeker applying to a job post, 
        where the evaluation details are sent to ChatGPT for generating a candidate status, profile synopsis, 
        and optimal job matches. Mocked methods simulate ChatGPT responses to confirm that the data is 
        correctly processed, saved in the Evaluation_Summary model, and stored in the session. 

        The test asserts:
        - Successful redirection to the job seeker report page.
        - Correct data storage in Evaluation_Summary, including candidate status, profile synopsis, and job matches.
        - Proper creation of foreign key relationships.
        - Storage of the evaluation summary ID in the session.
        - Expected calls to ChatGPT integration methods with correct arguments.
    """
        # Set mock return values
        mock_candidate_status.return_value = "Recommended"
        mock_profile_synopsis.return_value = "Professional and reliable."
        mock_optimal_job_matches.return_value = "Software Engineer, Data Analyst"

        # Perform POST request to the view
        response = self.client.post(self.url)

        # Check redirection to job_seeker_report
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('job_seeker_report'))

        # Check that Evaluation_Summary entry was created with expected values
        evaluation_summary = models.Evaluation_Summary.objects.get(USER_ID=self.user_info)
        
        # Assertions to verify stored data in Evaluation_Summary
        self.assertEqual(evaluation_summary.CANDIDATE_STATUS, "Recommended")
        self.assertEqual(evaluation_summary.PROFILE_SYNOPSIS, "Professional and reliable.")
        self.assertEqual(evaluation_summary.OPTIMAL_JOB_MATCHES, "Software Engineer, Data Analyst")
        self.assertEqual(evaluation_summary.USER_ID, self.user_info)
        self.assertEqual(evaluation_summary.JOB_SEEKER_ID, self.job_seeker)
        self.assertEqual(evaluation_summary.JOB_POST_ID, self.job_post)
        self.assertEqual(evaluation_summary.ASSESSMENT_ID, self.assessment)
        self.assertEqual(evaluation_summary.PERSONALITY_ASSESSMENT_REPORT_ID, self.personality_assessment_report)
        self.assertEqual(evaluation_summary.COGNITIVE_ASSESSMENT_RESULT_ID, self.cognitive_assessment_result)
        self.assertEqual(evaluation_summary.TECHNICAL_ASSESSMENT_RESULT_ID, self.technical_assessment_result)

        # Check if the session variable for EVALUATION_SUMMARY_ID is set
        self.assertIn('EVALUATION_SUMMARY_ID', self.client.session)
        self.assertEqual(self.client.session['EVALUATION_SUMMARY_ID'], str(evaluation_summary.EVALUATION_SUMMARY_ID))

        # Check if mocks were called with expected arguments
        mock_candidate_status.assert_called_once_with(ANY, self.job_post.JOB_POSITION)
        mock_profile_synopsis.assert_called_once_with(ANY)
        mock_optimal_job_matches.assert_called_once_with(ANY)
