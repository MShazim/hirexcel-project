from django.contrib import admin
from .models import (

    User_Information, 
    Job_Seeker, Job_Seeker_Education, Job_Seeker_Work_Experience, 
    Recruiter,Job_Position_Criteria, Job_Posting,
    Assessment, Job_Seeker_Assessment,
    Personality_Assessment,
    DISC_Assessment,DISC_Questions_Dataset, DISC_Score_Calculation_Dataset,DISC_Assessment_Answer,DISC_Characteristics_Dataset,DISC_Assessment_Result,
    BigFive_Assessment,BigFive_Questions_Dataset,BigFive_Assessment_Answers,BigFive_Characteristics_Dataset,BigFive_Assessment_Result,
    Personality_Assessment_Report,
    Cognitive_Assessment,
    Cognitive_NVI_Questions_Dataset,Cognitive_NVI_Answers_Dataset,
    Cognitive_VI_Question_Dataset,Cognitive_VI_Answers_Dataset,
    Cognitive_Assessment_Results,
    Technical_Assessment,
    Technical_Questions_Dataset,Technical_Answers_Dataset,
    Technical_Assessment_Result
)

class UserInformationAdmin(admin.ModelAdmin):
    list_display = ('USER_ID', 'FIRST_NAME', 'LAST_NAME', 'EMAIL', 'PASSWORD', 'CITY', 'COUNTRY', 'PHONE_NUMBER')

class JobSeekerAdmin(admin.ModelAdmin):
    list_display = ('JOB_SEEKER_ID', 'USER_ID', 'LINKEDIN_PROFILE_URL', 'GITHUB_PROFILE_URL', 'RESUME_UPLOAD')

class JobSeekerEducationAdmin(admin.ModelAdmin):
    list_display = ('JOB_SEEKER_EDUCATION_ID', 'JOB_SEEKER_ID', 'INSTITUTION_NAME', 'PROGRAM', 'START_DATE', 'END_DATE', 'DEGREE')

class JobSeekerWorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('JOB_SEEKER_WE_ID', 'JOB_SEEKER_ID', 'COMPANY_NAME', 'DESIGNATION', 'START_DATE', 'END_DATE')

class RecruiterAdmin(admin.ModelAdmin):
    list_display = ('RECRUITER_ID', 'USER_ID', 'COMPANY_NAME', 'COMPANY_WEBSITE', 'INDUSTRY', 'COMPANY_SIZE')

# Custom admin class for Job_Position_Criteria
class JobPositionCriteriaAdmin(admin.ModelAdmin):
    list_display = ('JPC_ID', 'CATEGORY', 'JOB_POSITION', 'PERSONALITY_TRAITS', 'COGNITIVE_SKILLS', 'EMOTIONAL_INTELLIGENCE')

class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('JOB_POST_ID', 'TITLE', 'DESCRIPTION', 'RECRUITER_ID', 'JPC_ID', 'CITY', 'COUNTRY', 'JOB_TYPE', 'JOB_POSITION', 'PERSONALITY_TRAITS', 'REQUIRED_SKILLS', 'REQUIRED_QUALIFICATIONS', 'EXPERIENCE_REQUIREMENTS', 'REQUIRED_ASSESSMENTS', 'TEST_CRITERIA')

class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('ASSESSMENT_ID', 'ASSESSMENT_CATEGORY', 'ASSESSMENT_SUB_TYPE', 'PASSING_SCORE', 'REQUIRED_COMPLETION_TIME')

class JobSeekerAssessmentAdmin(admin.ModelAdmin):
    list_display = ('JOB_SEEKER_ASSESSMENT_ID', 'JOB_SEEKER_ID', 'JOB_POST_ID', 'ASSESSMENT_ID', 'NAME', 'ASSESSMENT_TYPE', 'ASSESSMENT_ONGOING_STATUS', 'COMPLETION_TIME')

class PersonalityAssessmentAdmin(admin.ModelAdmin):
    list_display = ('PERSONALITY_ASSESSMENT_ID', 'JOB_SEEKER_ASSESSMENT_ID', 'PERSONALITY_TEST_TYPE')

class DISCAssessmentAdmin(admin.ModelAdmin):
    list_display = ('DISC_ASSESSMENT_ID', 'PERSONALITY_ASSESSMENT_ID')

# Custom admin class for Disc_Questions_Dataset
class DiscQuestionsDatasetAdmin(admin.ModelAdmin):
    list_display = ('DISC_PROFILE_ID', 'QUESTION', 'A', 'B', 'C', 'D')

# Custom admin class for Disc_Score_Calculation_Dataset
class DiscScoreCalculationDatasetAdmin(admin.ModelAdmin):
    list_display = ('DISC_PROFILE_ID', 'D', 'I', 'S', 'C')

class DISCAssessmentAnswerAdmin(admin.ModelAdmin):
    list_display = ('DISC_ASSESSMENT_ANS_ID', 'DISC_ASSESSMENT_ID', 'DISC_PROFILE_ID', 'DISC_PROFILE_SCORE_ID', 'JOB_SEEKER_ANS', 'DISC_PROFILE')

class DISCCharacteristicsDatasetAdmin(admin.ModelAdmin):
    list_display = ('DISC_CHARACTERISTIC_ID', 'DISC_CATEGORY', 'PERSONALITY_TRAIT', 'COGNITIVE_ABILITY', 'EMOTIONAL_REGULATION', 'TENDENCIES', 'WEAKNESSES', 'BEHAVIOUR', 'MOTIVATED_BY')

class DISCAssessmentResultAdmin(admin.ModelAdmin):
    list_display = ('DISC_ASSESSMENT_RESULT_ID', 'DISC_ASSESSMENT_ID', 'DISC_CATEGORY', 'SCORE')

class BigFiveAssessmentAdmin(admin.ModelAdmin):
    list_display = ('BIG_FIVE_ASSESSMENT_ID', 'PERSONALITY_ASSESSMENT_ID')

class BigFiveQuestionsDatasetAdmin(admin.ModelAdmin):
    list_display = ('DIMENSION', 'DIMENSION_ID', 'QUESTION', 'OPTION1', 'OPTION2', 'OPTION3', 'OPTION4', 'OPTION5')

class BigFiveCharacteristicsDatasetAdmin(admin.ModelAdmin):
    list_display = ('BIG_FIVE_CHAR_ID', 'DIMENSIONS', 'RANGES', 'CATEGORIES', 'PERSONALITY', 'DESCRIPTION', 'WORKPLACE_BEHAVIOR')

class BigFiveAssessmentAnswersAdmin(admin.ModelAdmin):
    list_display = ('BIG_FIVE_ASSESSMENT_ANS_ID', 'BIG_FIVE_ASSESSMENT_ID', 'DIMENSION_ID', 'JOB_SEEKER_ANS')

class BigFiveAssessmentResultAdmin(admin.ModelAdmin):
    list_display = ('BIG_FIVE_ASSESSMENT_RESULT_ID', 'BIG_FIVE_ASSESSMENT_ID', 'DIMENSIONS', 'SCORE')

class PersonalityAssessmentReportAdmin(admin.ModelAdmin):
    list_display = ('PERSONALITY_ASSESSMENT_REPORT_ID', 'PERSONALITY_ASSESSMENT_ID', 'JOB_SEEKER_ASSESSMENT_ID', 'BIG_FIVE_ASSESSMENT_ID', 'DISC_ASSESSMENT_ID')

class CognitiveAssessmentAdmin(admin.ModelAdmin):
    list_display = ('COGNITIVE_ASSESSMENT_ID', 'JOB_SEEKER_ASSESSMENT_ID', 'COGNITIVE_ASSESSMENT_TYPE')

# Custom admin class for NVI_Questions_Dataset
class CognitiveNVIQuestionsDatasetAdmin(admin.ModelAdmin):
    list_display = ('NVI_IMAGE_QUESTION_ID', 'IMAGE', 'OPTION1', 'OPTION2', 'OPTION3', 'OPTION4', 'OPTION5', 'OPTION6', 'OPTION7', 'OPTION8', 'ANSWERS')

class CognitiveNVIAnswersDatasetAdmin(admin.ModelAdmin):
    list_display = ('COGNITIVE_NVI_ANS_ID', 'COGNITIVE_ASSESSMENT_ID', 'NVI_IMAGE_QUESTION_ID', 'JOB_SEEKER_ANS', 'IS_CORRECT')

class CognitiveVIQuestionDatasetAdmin(admin.ModelAdmin):
    list_display = ('VI_QUESTION_ID', 'QUESTION', 'OPTION1', 'OPTION2', 'OPTION3', 'OPTION4', 'OPTION5', 'OPTION6', 'OPTION7', 'OPTION8', 'ANSWER')

class CognitiveVIAnswersDatasetAdmin(admin.ModelAdmin):
    list_display = ('COGNITIVE_VI_ANS_ID', 'COGNITIVE_ASSESSMENT_ID', 'VI_QUESTION_ID', 'JOB_SEEKER_ANS', 'IS_CORRECT')

class CognitiveAssessmentResultsAdmin(admin.ModelAdmin):
    list_display = ('COGNITIVE_ASSESSMENT_RESULT_ID', 'COGNITIVE_ASSESSMENT_ID', 'COGNITIVE_VI_SCORE', 'COGNITIVE_NVI_SCORE')

class TechnicalAssessmentAdmin(admin.ModelAdmin):
    list_display = ('TECHNICAL_ASSESSMENT_ID', 'JOB_SEEKER_ASSESSMENT_ID', 'TECHNICAL_ASSESSMENT_LEVEL')

# Custom admin class for Technical_Questions_Dataset
class TechnicalQuestionsDatasetAdmin(admin.ModelAdmin):
    list_display = ('TECH_ID', 'JOB_POSITION', 'TEST_LEVEL', 'QUESTION', 'ANSWER', 'A', 'B', 'C', 'D')

class TechnicalAnswersDatasetAdmin(admin.ModelAdmin):
    list_display = ('TECH_ANS_ID', 'TECH_ID', 'TECHNICAL_ASSESSMENT_ID', 'JOB_SEEKER_ANS', 'IS_CORRECT')

class TechnicalAssessmentResultAdmin(admin.ModelAdmin):
    list_display = ('TECHNICAL_ASSESSMENT_RESULT_ID', 'TECHNICAL_ASSESSMENT_ID', 'SCORE')


# Register the models with the custom admin classes
admin.site.register(User_Information, UserInformationAdmin)

admin.site.register(Job_Seeker, JobSeekerAdmin)
admin.site.register(Job_Seeker_Education, JobSeekerEducationAdmin)
admin.site.register(Job_Seeker_Work_Experience, JobSeekerWorkExperienceAdmin)

admin.site.register(Recruiter, RecruiterAdmin)
admin.site.register(Job_Position_Criteria, JobPositionCriteriaAdmin)
admin.site.register(Job_Posting, JobPostingAdmin)

admin.site.register(Assessment, AssessmentAdmin)
admin.site.register(Job_Seeker_Assessment, JobSeekerAssessmentAdmin)

admin.site.register(Personality_Assessment, PersonalityAssessmentAdmin)

admin.site.register(DISC_Assessment, DISCAssessmentAdmin)
admin.site.register(DISC_Questions_Dataset, DiscQuestionsDatasetAdmin)
admin.site.register(DISC_Score_Calculation_Dataset, DiscScoreCalculationDatasetAdmin)
admin.site.register(DISC_Assessment_Answer, DISCAssessmentAnswerAdmin)
admin.site.register(DISC_Characteristics_Dataset, DISCCharacteristicsDatasetAdmin)
admin.site.register(DISC_Assessment_Result, DISCAssessmentResultAdmin)

admin.site.register(BigFive_Assessment, BigFiveAssessmentAdmin)
admin.site.register(BigFive_Questions_Dataset, BigFiveQuestionsDatasetAdmin)
admin.site.register(BigFive_Characteristics_Dataset, BigFiveCharacteristicsDatasetAdmin)
admin.site.register(BigFive_Assessment_Answers, BigFiveAssessmentAnswersAdmin)
admin.site.register(BigFive_Assessment_Result, BigFiveAssessmentResultAdmin)

admin.site.register(Personality_Assessment_Report, PersonalityAssessmentReportAdmin)

admin.site.register(Cognitive_Assessment, CognitiveAssessmentAdmin)

admin.site.register(Cognitive_NVI_Questions_Dataset, CognitiveNVIQuestionsDatasetAdmin)
admin.site.register(Cognitive_NVI_Answers_Dataset, CognitiveNVIAnswersDatasetAdmin)

admin.site.register(Cognitive_VI_Question_Dataset, CognitiveVIQuestionDatasetAdmin)
admin.site.register(Cognitive_VI_Answers_Dataset, CognitiveVIAnswersDatasetAdmin)

admin.site.register(Cognitive_Assessment_Results, CognitiveAssessmentResultsAdmin)

admin.site.register(Technical_Assessment, TechnicalAssessmentAdmin)

admin.site.register(Technical_Questions_Dataset, TechnicalQuestionsDatasetAdmin)
admin.site.register(Technical_Answers_Dataset, TechnicalAnswersDatasetAdmin)

admin.site.register(Technical_Assessment_Result, TechnicalAssessmentResultAdmin)

