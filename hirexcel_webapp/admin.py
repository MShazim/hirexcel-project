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
    Technical_Assessment_Result,
    Evaluation_Summary
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
    list_display = ('JPC_ID', 'CATEGORY', 'JOB_POSITION', 'PERSONALITY_TRAITS', 'COGNITIVE_SKILLS', 'EMOTIONAL_INTELLIGENCE', 'COGNITIVE_WEIGHTAGE', 'TECHNICAL_WEIGHTAGE')

class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('JOB_POST_ID', 'TITLE', 'DESCRIPTION', 'RECRUITER_ID', 'CITY', 'COUNTRY', 'JOB_TYPE', 'JOB_POSITION', 'PERSONALITY_TRAITS', 'REQUIRED_SKILLS', 'REQUIRED_QUALIFICATIONS', 'EXPERIENCE_REQUIREMENTS', 'REQUIRED_ASSESSMENTS', 'COGNITIVE_WEIGHTAGE', 'TECHNICAL_WEIGHTAGE', 'TECHNICAL_ASSESSMENT_LEVEL' )

class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('ASSESSMENT_ID', 'JOB_POST_ID', 'COGNITIVE_WEIGHTAGE', 'TECHNICAL_WEIGHTAGE', 'TECHNICAL_ASSESSMENT_LEVEL')

class JobSeekerAssessmentAdmin(admin.ModelAdmin):
    list_display = ('JOB_SEEKER_ASSESSMENT_ID', 'JOB_SEEKER_ID', 'JOB_POST_ID', 'ASSESSMENT_ID', 'NAME', 'ASSESSMENT_TYPE', 'TOTAL_COMPLETION_TIME_REQUIRED')

class PersonalityAssessmentAdmin(admin.ModelAdmin):
    list_display = ('PERSONALITY_ASSESSMENT_ID', 'JOB_SEEKER_ASSESSMENT_ID')

class DISCAssessmentAdmin(admin.ModelAdmin):
    list_display = ('DISC_ASSESSMENT_ID', 'PERSONALITY_ASSESSMENT_ID', 'DISC_COMPLETION_TIME_REQUIRED')

# Custom admin class for DISC_Questions_Dataset
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
    list_display = ('DISC_ASSESSMENT_RESULT_ID', 'DISC_ASSESSMENT_ID', 'DISC_CATEGORY', 'DOMINANCE_SCORE', 'INFLUENCING_SCORE', 'STEADINESS_SCORE', 'CONCIENTIOUSNESS_SCORE', 'TOTAL_DISC_COMPLETION_TIME')

class BigFiveAssessmentAdmin(admin.ModelAdmin):
    list_display = ('BIGFIVE_ASSESSMENT_ID', 'PERSONALITY_ASSESSMENT_ID', 'BIGFIVE_COMPLETION_TIME_REQUIRED')

class BigFiveQuestionsDatasetAdmin(admin.ModelAdmin):
    list_display = ('DIMENSION', 'DIMENSION_ID', 'QUESTION', 'OPTION1', 'OPTION2', 'OPTION3', 'OPTION4', 'OPTION5', 'OPTION6')

class BigFiveCharacteristicsDatasetAdmin(admin.ModelAdmin):
    list_display = ('BIGFIVE_CHAR_ID', 'DIMENSION', 'RANGE', 'CATEGORY', 'PERSONALITY', 'DESCRIPTION', 'WORKPLACE_BEHAVIOUR')

class BigFiveAssessmentAnswersAdmin(admin.ModelAdmin):
    list_display = ('BIGFIVE_ASSESSMENT_ANS_ID', 'BIGFIVE_ASSESSMENT_ID', 'DIMENSION_ID', 'DIMENSION', 'JOB_SEEKER_ANS')

class BigFiveAssessmentResultAdmin(admin.ModelAdmin):
    list_display = ('BIGFIVE_ASSESSMENT_RESULT_ID', 'BIGFIVE_ASSESSMENT_ID', 'DIMENSION', 'OPENNESS_SCORE', 'CONCIENTIOUSNESS_SCORE', 'EXTRAVERSION_SCORE', 'AGREEABLENESS_SCORE', 'NEUROTICISM_SCORE')

class PersonalityAssessmentReportAdmin(admin.ModelAdmin):
    list_display = ('PERSONALITY_ASSESSMENT_REPORT_ID', 'PERSONALITY_ASSESSMENT_ID', 'JOB_SEEKER_ASSESSMENT_ID', 'BIG_FIVE_ASSESSMENT_ID', 'DISC_ASSESSMENT_ID', 'DISC_CATEGORY', 'DISC_PERSONALITY_TRAIT', 'DISC_COGNITIVE_ABILITY', 'DISC_EMOTIONAL_REGULATION', 'DISC_TENDENCIES', 'DISC_WEAKNESSES', 'DISC_BEHAVIOUR', 'DISC_MOTIVATED_BY', 
                    'BIGFIVE_OPENNESS_SCORE', 'BIGFIVE_OPENNESS_CATEGORY', 'BIGFIVE_OPENNESS_PERSONALITY', 'BIGFIVE_OPENNESS_DESCRIPTION', 'BIGFIVE_OPENNESS_WORKPLACE_BEHAVIOUR', 
                    'BIGFIVE_CONCIENTIOUSNESS_SCORE', 'BIGFIVE_CONCIENTIOUSNESS_CATEGORY', 'BIGFIVE_CONCIENTIOUSNESS_PERSONALITY', 'BIGFIVE_CONCIENTIOUSNESS_DESCRIPTION', 'BIGFIVE_CONCIENTIOUSNESS_WORKPLACE_BEHAVIOUR',
                    'BIGFIVE_EXTRAVERSION_SCORE', 'BIGFIVE_EXTRAVERSION_CATEGORY', 'BIGFIVE_EXTRAVERSION_PERSONALITY', 'BIGFIVE_EXTRAVERSION_DESCRIPTION', 'BIGFIVE_EXTRAVERSION_WORKPLACE_BEHAVIOUR',
                    'BIGFIVE_AGREEABLENESS_SCORE', 'BIGFIVE_AGREEABLENESS_CATEGORY', 'BIGFIVE_AGREEABLENESS_PERSONALITY', 'BIGFIVE_AGREEABLENESS_DESCRIPTION', 'BIGFIVE_AGREEABLENESS_WORKPLACE_BEHAVIOUR',
                    'BIGFIVE_NEUROTICISM_SCORE', 'BIGFIVE_NEUROTICISM_CATEGORY', 'BIGFIVE_NEUROTICISM_PERSONALITY', 'BIGFIVE_NEUROTICISM_DESCRIPTION', 'BIGFIVE_NEUROTICISM_WORKPLACE_BEHAVIOUR'
                    )

class CognitiveAssessmentAdmin(admin.ModelAdmin):
    list_display = ('COGNITIVE_ASSESSMENT_ID', 'JOB_SEEKER_ASSESSMENT_ID', 'COGNITIVE_COMPLETION_TIME_REQUIRED')

class CognitiveNVIQuestionsDatasetAdmin(admin.ModelAdmin):
    list_display = ('NVI_IMAGE_QUESTION_ID', 'IMAGE', 'OPTION1', 'OPTION2', 'OPTION3', 'OPTION4', 'OPTION5', 'OPTION6', 'OPTION7', 'OPTION8', 'ANSWERS')

class CognitiveNVIAnswersDatasetAdmin(admin.ModelAdmin):
    list_display = ('COGNITIVE_NVI_ANS_ID', 'COGNITIVE_ASSESSMENT_ID', 'NVI_IMAGE_QUESTION_ID', 'JOB_SEEKER_ANS', 'IS_CORRECT')

class CognitiveVIQuestionDatasetAdmin(admin.ModelAdmin):
    list_display = ('VI_QUESTION_ID', 'QUESTION', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'ANSWER')

class CognitiveVIAnswersDatasetAdmin(admin.ModelAdmin):
    list_display = ('COGNITIVE_VI_ANS_ID', 'COGNITIVE_ASSESSMENT_ID', 'VI_QUESTION_ID', 'JOB_SEEKER_ANS', 'IS_CORRECT')

class CognitiveAssessmentResultsAdmin(admin.ModelAdmin):
    list_display = ('COGNITIVE_ASSESSMENT_RESULT_ID', 'COGNITIVE_ASSESSMENT_ID', 'COGNITIVE_VI_SCORE', 'COGNITIVE_NVI_SCORE' ,'TOTAL_COGNITIVE_SCORE', 'VI_COMPLETION_TIME', 'NVI_COMPLETION_TIME', 'TOTAL_COGNITIVE_COMPLETION_TIME')

class TechnicalAssessmentAdmin(admin.ModelAdmin):
    list_display = ('TECHNICAL_ASSESSMENT_ID', 'JOB_SEEKER_ASSESSMENT_ID', 'TECHNICAL_ASSESSMENT_LEVEL', 'TECHNICAL_COMPLETION_TIME_REQUIRED')

class TechnicalQuestionsDatasetAdmin(admin.ModelAdmin):
    list_display = ('TECH_ID', 'JOB_POSITION', 'TEST_LEVEL', 'QUESTION', 'ANSWER', 'A', 'B', 'C', 'D')

class TechnicalAnswersDatasetAdmin(admin.ModelAdmin):
    list_display = ('TECH_ANS_ID', 'TECH_ID', 'TECHNICAL_ASSESSMENT_ID', 'JOB_SEEKER_ANS', 'IS_CORRECT')

class TechnicalAssessmentResultAdmin(admin.ModelAdmin):
    list_display = ('TECHNICAL_ASSESSMENT_RESULT_ID', 'TECHNICAL_ASSESSMENT_ID', 'TOTAL_TECH_SCORE', 'TOTAL_TECHNICAL_COMPLETION_TIME')

class EvaluationSummaryAdmin(admin.ModelAdmin):
    list_display = ('EVALUATION_SUMMARY_ID', 'USER_ID', 'JOB_SEEKER_ID', 'JOB_POST_ID', 'ASSESSMENT_ID', 'PERSONALITY_ASSESSMENT_REPORT_ID', 'COGNITIVE_ASSESSMENT_RESULT_ID', 'TECHNICAL_ASSESSMENT_RESULT_ID', 'CANDIDATE_STATUS', 'PROFILE_SYNOPSIS','OPTIMAL_JOB_MATCHES', 'EVALUATION_SUMMARY')



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

admin.site.register(Evaluation_Summary, EvaluationSummaryAdmin)