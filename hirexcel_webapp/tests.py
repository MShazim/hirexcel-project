from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from hirexcel_webapp.models import (
    User_Information,
    Job_Seeker,
    Recruiter,
    Job_Posting,
    Assessment,
    Job_Seeker_Assessment,
    Personality_Assessment,
    Personality_Assessment_Report,
    Cognitive_Assessment,
    Cognitive_Assessment_Results,
    Technical_Assessment,
    Technical_Assessment_Result,
    DISC_Assessment,
    BigFive_Assessment,
    Evaluation_Summary
)
from hirexcel_webapp.utils.chatgpt_integration import ChatGPTIntegration
from hirexcel_webapp import views

class ProcessAssessmentAndGenerateSummaryTestCase(TestCase):
    def setUp(self):
        # Create necessary data and relationships
        self.user_info = User_Information.objects.create(
            USER_ID="123456789", FIRST_NAME="Test", LAST_NAME="User",
            EMAIL="testuser@example.com", PASSWORD="password", PHONE_NUMBER="1234567890"
        )
        self.recruiter = Recruiter.objects.create(
            RECRUITER_ID="987654321", USER_ID=self.user_info, COMPANY_NAME="Test Company",
            COMPANY_WEBSITE="https://testcompany.com"
        )
        self.job_seeker = Job_Seeker.objects.create(
            JOB_SEEKER_ID="876543210", USER_ID=self.user_info
        )
        self.job_post = Job_Posting.objects.create(
            JOB_POST_ID="111111111", TITLE="Software Engineer", RECRUITER_ID=self.recruiter,
            CITY="City", COUNTRY="Country", JOB_TYPE="Full-Time", JOB_POSITION="Developer",
            PERSONALITY_TRAITS="Analytical", REQUIRED_SKILLS="Python",
            REQUIRED_QUALIFICATIONS="Bachelor's Degree", EXPERIENCE_REQUIREMENTS="2 Years",
            REQUIRED_ASSESSMENTS="DISC, BigFive", COGNITIVE_WEIGHTAGE="50",
            TECHNICAL_WEIGHTAGE="50", TECHNICAL_ASSESSMENT_LEVEL="Intermediate"
        )
        self.assessment = Assessment.objects.create(
            ASSESSMENT_ID="222222222", JOB_POST_ID=self.job_post,
            COGNITIVE_WEIGHTAGE="50", TECHNICAL_WEIGHTAGE="50",
            TECHNICAL_ASSESSMENT_LEVEL="Intermediate"
        )
        self.job_seeker_assessment = Job_Seeker_Assessment.objects.create(
            JOB_SEEKER_ASSESSMENT_ID="333333333", JOB_SEEKER_ID=self.job_seeker,
            JOB_POST_ID=self.job_post, ASSESSMENT_ID=self.assessment,
            NAME="Assessment Name", ASSESSMENT_TYPE="DISC",
            TOTAL_COMPLETION_TIME_REQUIRED="60 minutes"
        )
        self.personality_assessment = Personality_Assessment.objects.create(
            PERSONALITY_ASSESSMENT_ID="444444444", JOB_SEEKER_ASSESSMENT_ID=self.job_seeker_assessment
        )
        self.disc_assessment = DISC_Assessment.objects.create(
            DISC_ASSESSMENT_ID="555555555", PERSONALITY_ASSESSMENT_ID=self.personality_assessment,
            DISC_COMPLETION_TIME_REQUIRED="30 minutes"
        )
        self.bigfive_assessment = BigFive_Assessment.objects.create(
            BIGFIVE_ASSESSMENT_ID="666666666", PERSONALITY_ASSESSMENT_ID=self.personality_assessment,
            BIGFIVE_COMPLETION_TIME_REQUIRED="30 minutes"
        )
        self.personality_assessment_report = Personality_Assessment_Report.objects.create(
            PERSONALITY_ASSESSMENT_REPORT_ID="777777777", PERSONALITY_ASSESSMENT_ID=self.personality_assessment,
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
        self.cognitive_assessment = Cognitive_Assessment.objects.create(
            COGNITIVE_ASSESSMENT_ID="888888888", JOB_SEEKER_ASSESSMENT_ID=self.job_seeker_assessment,
            COGNITIVE_COMPLETION_TIME_REQUIRED="45 minutes"
        )
        self.cognitive_assessment_result = Cognitive_Assessment_Results.objects.create(
            COGNITIVE_ASSESSMENT_RESULT_ID="999999999", COGNITIVE_ASSESSMENT_ID=self.cognitive_assessment,
            COGNITIVE_VI_SCORE=60, COGNITIVE_NVI_SCORE=65, TOTAL_COGNITIVE_SCORE=62,
            COGNITIVE_SCORE_PERCENTAGE=60, VI_COMPLETION_TIME="10m", NVI_COMPLETION_TIME="15m",
            TOTAL_COGNITIVE_COMPLETION_TIME="25m"
        )
        self.technical_assessment = Technical_Assessment.objects.create(
            TECHNICAL_ASSESSMENT_ID="101010101", JOB_SEEKER_ASSESSMENT_ID=self.job_seeker_assessment,
            TECHNICAL_ASSESSMENT_LEVEL="Intermediate", TECHNICAL_COMPLETION_TIME_REQUIRED="30 minutes"
        )
        self.technical_assessment_result = Technical_Assessment_Result.objects.create(
            TECHNICAL_ASSESSMENT_RESULT_ID="111111111", TECHNICAL_ASSESSMENT_ID=self.technical_assessment,
            TOTAL_TECH_SCORE=80, TECH_SCORE_PERCENTAGE=75, TOTAL_TECHNICAL_COMPLETION_TIME="20m"
        )

        # Set up session data
        self.client = Client()
        session = self.client.session
        session['user_id'] = self.user_info.USER_ID
        session['JOB_SEEKER_ID'] = self.job_seeker.JOB_SEEKER_ID
        session['ASSESSMENT_ID'] = self.assessment.ASSESSMENT_ID
        session['PERSONALITY_ASSESSMENT_ID'] = self.personality_assessment_report.PERSONALITY_ASSESSMENT_REPORT_ID
        session['COGNITIVE_ASSESSMENT_ID'] = self.cognitive_assessment_result.COGNITIVE_ASSESSMENT_RESULT_ID
        session['TECHNICAL_ASSESSMENT_ID'] = self.technical_assessment_result.TECHNICAL_ASSESSMENT_RESULT_ID
        session.save()

    @patch.object(ChatGPTIntegration, 'generate_candidate_status', return_value="Recommended")
    @patch.object(ChatGPTIntegration, 'generate_profile_synopsis', return_value="This is a 100-word professional summary.")
    @patch.object(ChatGPTIntegration, 'generate_optimal_job_matches', return_value="Software Developer, Backend Engineer")
    def test_process_assessment_and_generate_summary_success(self, mock_candidate_status, mock_profile_synopsis, mock_job_matches):
        response = self.client.get(reverse('hirexcel_webapp:process_assessment_and_generate_summary'))
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('hirexcel_webapp:job_seeker_report'))

        evaluation_summary = Evaluation_Summary.objects.get(USER_ID=self.user_info)
        self.assertEqual(evaluation_summary.CANDIDATE_STATUS, "Recommended")
        self.assertEqual(evaluation_summary.PROFILE_SYNOPSIS, "This is a 100-word professional summary.")
        self.assertEqual(evaluation_summary.OPTIMAL_JOB_MATCHES, "Software Developer, Backend Engineer")

    @patch.object(ChatGPTIntegration, 'generate_candidate_status', side_effect=Exception("API Error"))
    @patch.object(ChatGPTIntegration, 'generate_profile_synopsis', return_value="unknown")
    @patch.object(ChatGPTIntegration, 'generate_optimal_job_matches', return_value="unknown")
    def test_process_assessment_and_generate_summary_api_failure(self, mock_candidate_status, mock_profile_synopsis, mock_job_matches):
        response = self.client.get('/process-assessment/')
        print("Status Code:", response.status_code)
        print("Content:", response.content)

        #response = self.client.get('/hirexcel_webapp/process-assessment/')

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('hirexcel_webapp:job_seeker_report'))

        evaluation_summary = Evaluation_Summary.objects.get(USER_ID=self.user_info)
        self.assertEqual(evaluation_summary.CANDIDATE_STATUS, "unknown")
        self.assertEqual(evaluation_summary.PROFILE_SYNOPSIS, "unknown")
        self.assertEqual(evaluation_summary.OPTIMAL_JOB_MATCHES, "unknown")
