from django.test import TestCase
from hirexcel_webapp import models
from django.core.files.uploadedfile import SimpleUploadedFile

class ModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Set up initial data for all models once for reuse across test cases.
        """

        # Create a User_Information instance
        cls.user_info = models.User_Information.objects.create(
            FIRST_NAME="Jane",
            LAST_NAME="Doe",
            EMAIL="janedoe@example.com",
            PASSWORD="securepassword",
            CITY="Los Angeles",
            COUNTRY="USA",
            PHONE_NUMBER="0987654321"
        )

        # Create a Job_Seeker instance
        cls.job_seeker = models.Job_Seeker.objects.create(
            USER_ID=cls.user_info,
            LINKEDIN_PROFILE_URL="https://linkedin.com/in/janedoe",
            GITHUB_PROFILE_URL="https://github.com/janedoe",
            RESUME_UPLOAD=SimpleUploadedFile("resume.pdf", b"Resume content", content_type="application/pdf")
        )

        # Create Job_Seeker_Education instance
        cls.job_seeker_education = models.Job_Seeker_Education.objects.create(
            JOB_SEEKER_ID=cls.job_seeker,
            INSTITUTION_NAME="Tech University",
            PROGRAM="Bachelor of Science",
            START_DATE="2020-01-01",
            END_DATE="2024-01-01",
            DEGREE="B.Sc."
        )

        # Create Job_Seeker_Work_Experience instance
        cls.job_seeker_work_experience = models.Job_Seeker_Work_Experience.objects.create(
            JOB_SEEKER_ID=cls.job_seeker,
            COMPANY_NAME="Tech Solutions",
            DESIGNATION="Software Engineer",
            START_DATE="2024-02-01",
            END_DATE="2025-02-01"
        )

        # Create Recruiter instance
        cls.recruiter = models.Recruiter.objects.create(
            USER_ID=cls.user_info,
            COMPANY_NAME="Tech Corp",
            COMPANY_WEBSITE="https://techcorp.com",
            INDUSTRY="Software",
            COMPANY_SIZE="200-500"
        )

        # Create Job_Posting instance
        cls.job_posting = models.Job_Posting.objects.create(
            TITLE="Software Engineer",
            DESCRIPTION="A job description here",
            RECRUITER_ID=cls.recruiter,
            CITY="New York",
            COUNTRY="USA",
            JOB_TYPE="Full-Time",
            JOB_POSITION="Engineer",
            PERSONALITY_TRAITS="Analytical",
            REQUIRED_SKILLS="Python, Django",
            REQUIRED_QUALIFICATIONS="B.Sc. in Computer Science",
            EXPERIENCE_REQUIREMENTS="2+ years",
            REQUIRED_ASSESSMENTS="DISC, BigFive",
            COGNITIVE_WEIGHTAGE="40",
            TECHNICAL_WEIGHTAGE="60",
            TECHNICAL_ASSESSMENT_LEVEL="Intermediate"
        )

        # Create Assessment instance
        cls.assessment = models.Assessment.objects.create(
            JOB_POST_ID=cls.job_posting,
            COGNITIVE_WEIGHTAGE="50",
            TECHNICAL_WEIGHTAGE="50",
            TECHNICAL_ASSESSMENT_LEVEL="Advanced"
        )
        
        cls.job_seeker_assessment = models.Job_Seeker_Assessment.objects.create(
            JOB_SEEKER_ID=cls.job_seeker,
            JOB_POST_ID=cls.job_posting,
            ASSESSMENT_ID=cls.assessment,
            NAME="Job Seeker Assessment",
            ASSESSMENT_TYPE="DISC",
            TOTAL_COMPLETION_TIME_REQUIRED="1 hour"
        )

        cls.personality_assessment = models.Personality_Assessment.objects.create(
            JOB_SEEKER_ASSESSMENT_ID=cls.job_seeker_assessment
        )

        cls.disc_assessment = models.DISC_Assessment.objects.create(
            PERSONALITY_ASSESSMENT_ID=cls.personality_assessment,
            DISC_COMPLETION_TIME_REQUIRED="30 minutes"
        )

        cls.bigfive_assessment = models.BigFive_Assessment.objects.create(
            PERSONALITY_ASSESSMENT_ID=cls.personality_assessment,
            BIGFIVE_COMPLETION_TIME_REQUIRED="30 minutes"
        )

        cls.personality_assessment_report = models.Personality_Assessment_Report.objects.create(
            PERSONALITY_ASSESSMENT_ID=cls.personality_assessment,
            JOB_SEEKER_ASSESSMENT_ID=cls.job_seeker_assessment,
            BIGFIVE_ASSESSMENT_ID=cls.bigfive_assessment,
            DISC_ASSESSMENT_ID=cls.disc_assessment,
            DISC_CATEGORY="High Dominance",
            DISC_PERSONALITY_TRAIT="Analytical",
            DISC_COGNITIVE_ABILITY="High",
            DISC_EMOTIONAL_REGULATION="Stable",
            DISC_TENDENCIES="Leader",
            DISC_WEAKNESSES="Impulsive",
            DISC_BEHAVIOUR="Direct",
            DISC_MOTIVATED_BY="Challenge",
            BIGFIVE_OPENNESS_SCORE=85,
            BIGFIVE_OPENNESS_CATEGORY="High",
            BIGFIVE_OPENNESS_PERSONALITY="Creative",
            BIGFIVE_OPENNESS_DESCRIPTION="Highly imaginative",
            BIGFIVE_OPENNESS_WORKPLACE_BEHAVIOUR="Innovative",
            BIGFIVE_CONCIENTIOUSNESS_SCORE=75,
            BIGFIVE_CONCIENTIOUSNESS_CATEGORY="Moderate",
            BIGFIVE_CONCIENTIOUSNESS_PERSONALITY="Organized",
            BIGFIVE_CONCIENTIOUSNESS_DESCRIPTION="Dependable",
            BIGFIVE_CONCIENTIOUSNESS_WORKPLACE_BEHAVIOUR="Detail-oriented",
            BIGFIVE_EXTRAVERSION_SCORE=70,
            BIGFIVE_EXTRAVERSION_CATEGORY="Moderate",
            BIGFIVE_EXTRAVERSION_PERSONALITY="Sociable",
            BIGFIVE_EXTRAVERSION_DESCRIPTION="Outgoing",
            BIGFIVE_EXTRAVERSION_WORKPLACE_BEHAVIOUR="Team player",
            BIGFIVE_AGREEABLENESS_SCORE=65,
            BIGFIVE_AGREEABLENESS_CATEGORY="Moderate",
            BIGFIVE_AGREEABLENESS_PERSONALITY="Trusting",
            BIGFIVE_AGREEABLENESS_DESCRIPTION="Cooperative",
            BIGFIVE_AGREEABLENESS_WORKPLACE_BEHAVIOUR="Collaborative",
            BIGFIVE_NEUROTICISM_SCORE=50,
            BIGFIVE_NEUROTICISM_CATEGORY="Low",
            BIGFIVE_NEUROTICISM_PERSONALITY="Calm",
            BIGFIVE_NEUROTICISM_DESCRIPTION="Emotionally stable",
            BIGFIVE_NEUROTICISM_WORKPLACE_BEHAVIOUR="Resilient"
        )

        cls.cognitive_assessment = models.Cognitive_Assessment.objects.create(
            JOB_SEEKER_ASSESSMENT_ID=cls.job_seeker_assessment,
            COGNITIVE_COMPLETION_TIME_REQUIRED="45 minutes"
        )
        
        cls.cognitive_assessment_result = models.Cognitive_Assessment_Results.objects.create(
            COGNITIVE_ASSESSMENT_ID=cls.cognitive_assessment,
            COGNITIVE_VI_SCORE=80,
            COGNITIVE_NVI_SCORE=85,
            TOTAL_COGNITIVE_SCORE=82,
            COGNITIVE_SCORE_PERCENTAGE=80,
            VI_COMPLETION_TIME="20m",
            NVI_COMPLETION_TIME="25m",
            TOTAL_COGNITIVE_COMPLETION_TIME="45m"
        )

        cls.technical_assessment = models.Technical_Assessment.objects.create(
            JOB_SEEKER_ASSESSMENT_ID=cls.job_seeker_assessment,
            TECHNICAL_ASSESSMENT_LEVEL="Intermediate",
            TECHNICAL_COMPLETION_TIME_REQUIRED="30 minutes"
        )
        
        cls.technical_assessment_result = models.Technical_Assessment_Result.objects.create(
            TECHNICAL_ASSESSMENT_ID=cls.technical_assessment,
            TOTAL_TECH_SCORE=90,
            TECH_SCORE_PERCENTAGE=85,
            TOTAL_TECHNICAL_COMPLETION_TIME="30m"
        )

        cls.evaluation_summary = models.Evaluation_Summary.objects.create(
            USER_ID=cls.user_info,
            JOB_SEEKER_ID=cls.job_seeker,
            JOB_POST_ID=cls.job_posting,
            ASSESSMENT_ID=cls.assessment,
            PERSONALITY_ASSESSMENT_REPORT_ID=cls.personality_assessment_report,
            COGNITIVE_ASSESSMENT_RESULT_ID=cls.cognitive_assessment_result,
            TECHNICAL_ASSESSMENT_RESULT_ID=cls.technical_assessment_result,
            CANDIDATE_STATUS="Recommended",
            PROFILE_SYNOPSIS="Analytical and detail-oriented.",
            OPTIMAL_JOB_MATCHES="Data Scientist, Software Engineer"
        )

    def test_user_information_creation(self):
        """ Test User_Information model instance """
        user = self.user_info
        self.assertEqual(user.FIRST_NAME, "Jane")
        self.assertEqual(user.CITY, "Los Angeles")
        self.assertTrue(user.USER_ID.isdigit() and len(user.USER_ID) == 9)
        self.assertEqual(str(user), user.USER_ID)

    def test_job_seeker_creation(self):
        """ Test Job_Seeker model instance """
        job_seeker = self.job_seeker
        self.assertEqual(job_seeker.USER_ID, self.user_info)
        self.assertEqual(job_seeker.LINKEDIN_PROFILE_URL, "https://linkedin.com/in/janedoe")
        self.assertTrue(job_seeker.JOB_SEEKER_ID.isdigit() and len(job_seeker.JOB_SEEKER_ID) == 9)
        self.assertEqual(str(job_seeker), job_seeker.JOB_SEEKER_ID)

    def test_job_seeker_education_creation(self):
        """ Test Job_Seeker_Education model instance """
        education = self.job_seeker_education
        self.assertEqual(education.INSTITUTION_NAME, "Tech University")
        self.assertEqual(education.PROGRAM, "Bachelor of Science")
        self.assertTrue(education.JOB_SEEKER_EDUCATION_ID.isdigit() and len(education.JOB_SEEKER_EDUCATION_ID) == 9)
        self.assertEqual(str(education), education.JOB_SEEKER_EDUCATION_ID)

    def test_job_seeker_work_experience_creation(self):
        """ Test Job_Seeker_Work_Experience model instance """
        experience = self.job_seeker_work_experience
        self.assertEqual(experience.COMPANY_NAME, "Tech Solutions")
        self.assertEqual(experience.DESIGNATION, "Software Engineer")
        self.assertTrue(experience.JOB_SEEKER_WE_ID.isdigit() and len(experience.JOB_SEEKER_WE_ID) == 9)
        self.assertEqual(str(experience), experience.JOB_SEEKER_WE_ID)

    def test_recruiter_creation(self):
        """ Test Recruiter model instance """
        recruiter = self.recruiter
        self.assertEqual(recruiter.COMPANY_NAME, "Tech Corp")
        self.assertEqual(recruiter.COMPANY_WEBSITE, "https://techcorp.com")
        self.assertTrue(recruiter.RECRUITER_ID.isdigit() and len(recruiter.RECRUITER_ID) == 9)
        self.assertEqual(str(recruiter), recruiter.RECRUITER_ID)

    def test_job_posting_creation(self):
        """ Test Job_Posting model instance """
        job_post = self.job_posting
        self.assertEqual(job_post.TITLE, "Software Engineer")
        self.assertEqual(job_post.CITY, "New York")
        self.assertTrue(job_post.JOB_POST_ID.isdigit() and len(job_post.JOB_POST_ID) == 9)
        self.assertEqual(str(job_post), job_post.JOB_POST_ID)

    def test_assessment_creation(self):
        """ Test Assessment model instance """
        assessment = self.assessment
        self.assertEqual(assessment.COGNITIVE_WEIGHTAGE, "50")
        self.assertEqual(assessment.TECHNICAL_ASSESSMENT_LEVEL, "Advanced")
        self.assertTrue(assessment.ASSESSMENT_ID.isdigit() and len(assessment.ASSESSMENT_ID) == 9)
        self.assertEqual(str(assessment), assessment.ASSESSMENT_ID)

    def test_personality_assessment_creation(self):
        """ Test Personality_Assessment model instance """
        personality_assessment = self.personality_assessment
        self.assertEqual(personality_assessment.JOB_SEEKER_ASSESSMENT_ID, self.job_seeker_assessment)
        self.assertTrue(personality_assessment.PERSONALITY_ASSESSMENT_ID.isdigit())

    def test_disc_assessment_creation(self):
        """ Test DISC_Assessment model instance """
        disc_assessment = self.disc_assessment
        self.assertEqual(disc_assessment.PERSONALITY_ASSESSMENT_ID, self.personality_assessment)
        self.assertTrue(disc_assessment.DISC_ASSESSMENT_ID.isdigit())

    def test_bigfive_assessment_creation(self):
        """ Test BigFive_Assessment model instance """
        bigfive_assessment = self.bigfive_assessment
        self.assertEqual(bigfive_assessment.PERSONALITY_ASSESSMENT_ID, self.personality_assessment)
        self.assertTrue(bigfive_assessment.BIGFIVE_ASSESSMENT_ID.isdigit())

    def test_personality_assessment_report_creation(self):
        """ Test Personality_Assessment_Report model instance """
        report = self.personality_assessment_report
        self.assertEqual(report.DISC_CATEGORY, "High Dominance")
        self.assertTrue(report.PERSONALITY_ASSESSMENT_REPORT_ID.isdigit())

    def test_cognitive_assessment_creation(self):
        """ Test Cognitive_Assessment model instance """
        cognitive_assessment = self.cognitive_assessment
        self.assertEqual(cognitive_assessment.COGNITIVE_COMPLETION_TIME_REQUIRED, "45 minutes")
        self.assertTrue(cognitive_assessment.COGNITIVE_ASSESSMENT_ID.isdigit())

    def test_technical_assessment_creation(self):
        """ Test Technical_Assessment model instance """
        technical_assessment = self.technical_assessment
        self.assertEqual(technical_assessment.TECHNICAL_ASSESSMENT_LEVEL, "Intermediate")
        self.assertTrue(technical_assessment.TECHNICAL_ASSESSMENT_ID.isdigit())

    def test_evaluation_summary_creation(self):
        """ Test Evaluation_Summary model instance """
        summary = self.evaluation_summary
        self.assertEqual(summary.CANDIDATE_STATUS, "Recommended")
        self.assertEqual(summary.PROFILE_SYNOPSIS, "Analytical and detail-oriented.")
        self.assertTrue(summary.EVALUATION_SUMMARY_ID.isdigit())