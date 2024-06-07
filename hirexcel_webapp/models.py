import random
from django.db import models
from django.db import transaction

def generate_unique_id(model_class):
    while True:
        new_id = str(random.randint(100000000, 999999999))
        if not model_class.objects.filter(pk=new_id).exists():
            return new_id

# creating model for User_Information
class User_Information(models.Model):
    USER_ID = models.CharField(primary_key=True, editable=False, max_length=9)
    FIRST_NAME = models.CharField(max_length=100)
    LAST_NAME = models.CharField(max_length=100)
    EMAIL = models.EmailField()
    PASSWORD = models.CharField(max_length=100)
    CITY = models.CharField(max_length=100, blank=True, null=True)
    COUNTRY = models.CharField(max_length=100, blank=True, null=True)
    PHONE_NUMBER = models.CharField(max_length=15)

    def save(self, *args, **kwargs):
        # Check if User_Id is not set (i.e., for new instances)
        if not self.USER_ID:
            # Generate a unique ID and assign it to User_Id
            self.USER_ID = generate_unique_id(User_Information)
        # Ensure the save operation is atomic
        with transaction.atomic():
            super(User_Information, self).save(*args, **kwargs)
    
    # String representation of the model instance
    def __str__(self):
        return str(self.USER_ID)

# creating model for Job_Seeker
class Job_Seeker(models.Model):
    JOB_SEEKER_ID = models.CharField(primary_key=True, editable=False, max_length=9)
    USER_ID = models.ForeignKey(User_Information, on_delete=models.CASCADE)
    LINKEDIN_PROFILE_URL = models.URLField(blank=True, null=True)
    GITHUB_PROFILE_URL = models.URLField(blank=True, null=True)
    RESUME_UPLOAD = models.FileField(upload_to='hirexcel_webapp/JobSeekerResumes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.JOB_SEEKER_ID:
            self.JOB_SEEKER_ID = generate_unique_id(Job_Seeker)
        with transaction.atomic():
            super(Job_Seeker, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.JOB_SEEKER_ID)
    
class Job_Seeker_Education(models.Model):
    JOB_SEEKER_EDUCATION_ID = models.CharField(primary_key=True, editable=False, max_length=9)
    JOB_SEEKER_ID = models.ForeignKey(Job_Seeker, on_delete=models.CASCADE)
    INSTITUTION_NAME = models.CharField(max_length=100)
    PROGRAM = models.CharField(max_length=100,blank=True, null=True)
    START_DATE = models.DateField()
    END_DATE = models.DateField( blank=True, null=True)
    DEGREE = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.JOB_SEEKER_EDUCATION_ID:
            self.JOB_SEEKER_EDUCATION_ID = generate_unique_id(Job_Seeker_Education)
        with transaction.atomic():
            super(Job_Seeker_Education, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.JOB_SEEKER_EDUCATION_ID)

class Job_Seeker_Work_Experience(models.Model):
    JOB_SEEKER_WE_ID = models.CharField(primary_key=True, editable=False, max_length=9)
    JOB_SEEKER_ID = models.ForeignKey(Job_Seeker, on_delete=models.CASCADE)
    COMPANY_NAME = models.CharField(max_length=100)
    DESIGNATION = models.CharField(max_length=100)
    START_DATE = models.DateField()
    END_DATE = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.JOB_SEEKER_WE_ID:
            self.JOB_SEEKER_WE_ID = generate_unique_id(Job_Seeker_Work_Experience)
        with transaction.atomic():
            super(Job_Seeker_Work_Experience, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.JOB_SEEKER_WE_ID)
    
class Recruiter(models.Model):
    RECRUITER_ID = models.CharField(primary_key=True, editable=False, max_length=9)
    USER_ID = models.ForeignKey(User_Information, on_delete=models.CASCADE)
    COMPANY_NAME = models.CharField(max_length=100)
    COMPANY_WEBSITE = models.URLField( blank=True, null=True)
    INDUSTRY = models.CharField(max_length=100, blank=True, null=True)
    COMPANY_SIZE = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.RECRUITER_ID:
            self.RECRUITER_ID = generate_unique_id(Recruiter)
        with transaction.atomic():
            super(Recruiter, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.RECRUITER_ID)

class Job_Position_Criteria(models.Model):
    JPC_ID = models.CharField(primary_key=True,max_length=10)
    CATEGORY = models.CharField(max_length=100)
    JOB_POSITION = models.CharField(max_length=100)
    PERSONALITY_TRAITS = models.CharField(max_length=100)
    COGNITIVE_SKILLS = models.CharField(max_length=100)
    EMOTIONAL_INTELLIGENCE = models.CharField(max_length=100)

    def __str__(self):
        return str(self.JPC_ID)

class Job_Posting(models.Model):
    JOB_POST_ID = models.CharField(primary_key=True, editable=False, max_length=9)
    TITLE = models.CharField(max_length=100)
    DESCRIPTION = models.TextField()
    RECRUITER_ID = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    JPC_ID = models.ForeignKey(Job_Position_Criteria, on_delete=models.CASCADE)
    CITY = models.CharField(max_length=100)
    COUNTRY = models.CharField(max_length=100)
    JOB_TYPE = models.CharField(max_length=100)
    JOB_POSITION = models.CharField(max_length=100)
    PERSONALITY_TRAITS = models.TextField()
    REQUIRED_SKILLS = models.TextField()
    REQUIRED_QUALIFICATIONS = models.TextField()
    EXPERIENCE_REQUIREMENTS = models.TextField()
    REQUIRED_ASSESSMENTS = models.TextField()
    TEST_CRITERIA = models.TextField( blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.JOB_POST_ID:
            self.JOB_POST_ID = generate_unique_id(Job_Posting)
        with transaction.atomic():
            super(Job_Posting, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.JOB_POST_ID)

class Assessment(models.Model):
    ASSESSMENT_ID = models.CharField(primary_key=True, editable=False, max_length=9)
    ASSESSMENT_CATEGORY = models.CharField(max_length=200)
    ASSESSMENT_SUB_TYPE = models.URLField( blank=True, null=True)
    PASSING_SCORE = models.CharField(max_length=100, blank=True, null=True)
    REQUIRED_COMPLETION_TIME = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.ASSESSMENT_ID:
            self.ASSESSMENT_ID = generate_unique_id(Assessment)
        with transaction.atomic():
            super(Assessment, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.ASSESSMENT_ID)

class Job_Seeker_Assessment(models.Model):
    JOB_SEEKER_ASSESSMENT_ID = models.CharField(primary_key=True, editable=False, max_length=9)
    JOB_SEEKER_ID = models.ForeignKey(Job_Seeker, on_delete=models.CASCADE)
    JOB_POST_ID = models.ForeignKey(Job_Posting, on_delete=models.CASCADE)
    ASSESSMENT_ID = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    NAME = models.CharField(max_length=100)
    ASSESSMENT_TYPE = models.CharField(max_length=100)
    ASSESSMENT_ONGOING_STATUS = models.CharField(max_length=100)
    COMPLETION_TIME = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.JOB_SEEKER_ASSESSMENT_ID:
            self.JOB_SEEKER_ASSESSMENT_ID = generate_unique_id(Job_Seeker_Assessment)
        with transaction.atomic():
            super(Job_Seeker_Assessment, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.JOB_SEEKER_ASSESSMENT_ID)
    
class Personality_Assessment(models.Model):
    PERSONALITY_ASSESSMENT_ID = models.CharField(primary_key=True, editable=False, max_length=9)
    JOB_SEEKER_ASSESSMENT_ID = models.ForeignKey(Job_Seeker_Assessment, on_delete=models.CASCADE)
    PERSONALITY_TEST_TYPE = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.PERSONALITY_ASSESSMENT_ID:
            self.PERSONALITY_ASSESSMENT_ID = generate_unique_id(Personality_Assessment)
        with transaction.atomic():
            super(Personality_Assessment, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.PERSONALITY_ASSESSMENT_ID)
    
class DISC_Assessment(models.Model):
    DISC_ASSESSMENT_ID = models.CharField(primary_key=True, editable=False, max_length=9)
    PERSONALITY_ASSESSMENT_ID = models.ForeignKey(Personality_Assessment, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.DISC_ASSESSMENT_ID:
            self.DISC_ASSESSMENT_ID = generate_unique_id(DISC_Assessment)
        with transaction.atomic():
            super(DISC_Assessment, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.DISC_ASSESSMENT_ID)
    
# creating model for disc questions datset
class DISC_Questions_Dataset(models.Model):
    DISC_PROFILE_ID = models.CharField(primary_key=True,max_length=10)
    QUESTION = models.TextField()
    A = models.CharField(max_length=100)
    B = models.CharField(max_length=100)
    C = models.CharField(max_length=100)
    D = models.CharField(max_length=100)

    def __str__(self):
        # String representation of the model instance
        return self.DISC_PROFILE_ID

# creating model for disc score calculation datset
class DISC_Score_Calculation_Dataset(models.Model):
    DISC_PROFILE_ID = models.CharField(primary_key=True,max_length=10)
    D = models.CharField(max_length=4)
    I = models.CharField(max_length=4)
    S = models.CharField(max_length=4)
    C = models.CharField(max_length=4)

    def __str__(self):
        # String representation of the model instance
        return self.DISC_PROFILE_ID
    
class DISC_Assessment_Answer(models.Model):
    DISC_ASSESSMENT_ANS_ID = models.CharField(primary_key=True, editable=False, max_length=9)
    DISC_ASSESSMENT_ID = models.ForeignKey(DISC_Assessment, on_delete=models.CASCADE)
    DISC_PROFILE_ID = models.ForeignKey(DISC_Questions_Dataset, on_delete=models.CASCADE)
    DISC_PROFILE_SCORE_ID = models.ForeignKey(DISC_Score_Calculation_Dataset, on_delete=models.CASCADE)
    JOB_SEEKER_ANS = models.CharField(max_length=100)
    DISC_PROFILE = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.DISC_ASSESSMENT_ANS_ID:
            self.DISC_ASSESSMENT_ANS_ID = generate_unique_id(DISC_Assessment_Answer)
        with transaction.atomic():
            super(DISC_Assessment_Answer, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.DISC_ASSESSMENT_ANS_ID)
    
class DISC_Characteristics_Dataset(models.Model):
    DISC_CHARACTERISTIC_ID = models.CharField(primary_key=True,max_length=10)
    DISC_CATEGORY = models.CharField(max_length=300)
    PERSONALITY_TRAIT = models.CharField(max_length=300)
    COGNITIVE_ABILITY = models.CharField(max_length=300)
    EMOTIONAL_REGULATION = models.CharField(max_length=300)
    TENDENCIES = models.CharField(max_length=300)
    WEAKNESSES = models.CharField(max_length=300)
    BEHAVIOUR = models.CharField(max_length=300)
    MOTIVATED_BY = models.CharField(max_length=300)

    def __str__(self):
        return self.DISC_CHARACTERISTIC_ID

class DISC_Assessment_Result(models.Model):
    DISC_ASSESSMENT_RESULT_ID = models.CharField(primary_key=True, editable=False, max_length=9)
    DISC_ASSESSMENT_ID = models.ForeignKey(DISC_Assessment, on_delete=models.CASCADE)
    DISC_CATEGORY = models.CharField(max_length=100)
    SCORE = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.DISC_ASSESSMENT_RESULT_ID:
            self.DISC_ASSESSMENT_RESULT_ID = generate_unique_id(DISC_Assessment_Result)
        with transaction.atomic():
            super(DISC_Assessment_Result, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.DISC_ASSESSMENT_RESULT_ID)

class BigFive_Assessment(models.Model):
    BIG_FIVE_ASSESSMENT_ID = models.CharField(primary_key=True, editable=False, max_length=9)
    PERSONALITY_ASSESSMENT_ID = models.ForeignKey(Personality_Assessment, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.BIG_FIVE_ASSESSMENT_ID:
            self.BIG_FIVE_ASSESSMENT_ID = generate_unique_id(BigFive_Assessment)
        with transaction.atomic():
            super(BigFive_Assessment, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.BIG_FIVE_ASSESSMENT_ID)

class BigFive_Questions_Dataset(models.Model):
    DIMENSION = models.CharField(max_length=100)
    DIMENSION_ID = models.CharField(primary_key=True,max_length=10)
    QUESTION = models.TextField()
    OPTION1 = models.CharField(max_length=100)
    OPTION2 = models.CharField(max_length=100)
    OPTION3 = models.CharField(max_length=100)
    OPTION4 = models.CharField(max_length=100)
    OPTION5 = models.CharField(max_length=100)

    def __str__(self):
        return str(self.DIMENSION_ID)
    
class BigFive_Assessment_Answers(models.Model):
    BIG_FIVE_ASSESSMENT_ANS_ID = models.CharField(primary_key=True, editable=False, max_length=9)
    BIG_FIVE_ASSESSMENT_ID = models.ForeignKey(BigFive_Assessment, on_delete=models.CASCADE)
    DIMENSION_ID = models.ForeignKey(BigFive_Questions_Dataset, on_delete=models.CASCADE)
    JOB_SEEKER_ANS = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.BIG_FIVE_ASSESSMENT_ANS_ID:
            self.BIG_FIVE_ASSESSMENT_ANS_ID = generate_unique_id(BigFive_Assessment_Answers)
        with transaction.atomic():
            super(BigFive_Assessment_Answers, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.BIG_FIVE_ASSESSMENT_ANS_ID)

class BigFive_Characteristics_Dataset(models.Model):
    BIG_FIVE_CHAR_ID = models.CharField(primary_key=True,max_length=10)
    DIMENSIONS = models.CharField(max_length=100)
    RANGES = models.CharField(max_length=100)
    CATEGORIES = models.CharField(max_length=100)
    PERSONALITY = models.CharField(max_length=100)
    DESCRIPTION = models.TextField()
    WORKPLACE_BEHAVIOR = models.TextField()

    def __str__(self):
        return str(self.BIG_FIVE_CHAR_ID)
    
class BigFive_Assessment_Result(models.Model):
    BIG_FIVE_ASSESSMENT_RESULT_ID = models.CharField(primary_key=True, editable=False, max_length=9)
    BIG_FIVE_ASSESSMENT_ID = models.ForeignKey(BigFive_Assessment, on_delete=models.CASCADE)
    DIMENSIONS = models.CharField(max_length=100)
    SCORE = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.BIG_FIVE_ASSESSMENT_RESULT_ID:
            self.BIG_FIVE_ASSESSMENT_RESULT_ID = generate_unique_id(BigFive_Assessment_Result)
        with transaction.atomic():
            super(BigFive_Assessment_Result, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.BIG_FIVE_ASSESSMENT_RESULT_ID)
    
class Personality_Assessment_Report(models.Model):
    PERSONALITY_ASSESSMENT_REPORT_ID = models.CharField(primary_key=True, editable=False, max_length=9)
    PERSONALITY_ASSESSMENT_ID =  models.ForeignKey(Personality_Assessment, on_delete=models.CASCADE)
    JOB_SEEKER_ASSESSMENT_ID = models.ForeignKey(Job_Seeker_Assessment, on_delete=models.CASCADE)
    BIG_FIVE_ASSESSMENT_ID = models.ForeignKey(BigFive_Assessment, on_delete=models.CASCADE)
    DISC_ASSESSMENT_ID = models.ForeignKey(DISC_Assessment, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.PERSONALITY_ASSESSMENT_REPORT_ID:
            self.PERSONALITY_ASSESSMENT_REPORT_ID = generate_unique_id(Personality_Assessment_Report)
        with transaction.atomic():
            super(Personality_Assessment_Report, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.PERSONALITY_ASSESSMENT_REPORT_ID)

class Cognitive_Assessment(models.Model):
    COGNITIVE_ASSESSMENT_ID = models.CharField(primary_key=True, editable=False, max_length=9)
    JOB_SEEKER_ASSESSMENT_ID = models.ForeignKey(Job_Seeker_Assessment, on_delete=models.CASCADE)
    COGNITIVE_ASSESSMENT_TYPE = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.COGNITIVE_ASSESSMENT_ID:
            self.COGNITIVE_ASSESSMENT_ID = generate_unique_id(Cognitive_Assessment)
        with transaction.atomic():
            super(Cognitive_Assessment, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.COGNITIVE_ASSESSMENT_ID)

# creating model for NVI questions datset
class Cognitive_NVI_Questions_Dataset(models.Model):
    # A unique identifier for each image question
    NVI_IMAGE_QUESTION_ID = models.CharField(primary_key=True,max_length=10)
    
    # A field to store the uploaded image file
    IMAGE = models.ImageField(upload_to='hirexcel_webapp/images/NVI_Questions_Dataset')
    
    # Fields for the various options
    OPTION1 = models.CharField(max_length=4)
    OPTION2 = models.CharField(max_length=4)
    OPTION3 = models.CharField(max_length=4)
    OPTION4 = models.CharField(max_length=4)
    OPTION5 = models.CharField(max_length=4)
    OPTION6 = models.CharField(max_length=4)
    OPTION7 = models.CharField(max_length=4)
    OPTION8 = models.CharField(max_length=4)
    
    # Field to store the correct answer
    ANSWERS = models.CharField(max_length=3)

    def __str__(self):
        # String representation of the model instance
        return self.NVI_IMAGE_QUESTION_ID

class Cognitive_NVI_Answers_Dataset(models.Model):
    COGNITIVE_NVI_ANS_ID = models.CharField(primary_key=True, editable=False, max_length=9)
    COGNITIVE_ASSESSMENT_ID = models.ForeignKey(Cognitive_Assessment, on_delete=models.CASCADE)
    NVI_IMAGE_QUESTION_ID = models.ForeignKey(Cognitive_NVI_Questions_Dataset, on_delete=models.CASCADE)
    JOB_SEEKER_ANS = models.CharField(max_length=100)
    IS_CORRECT = models.BooleanField()

    def save(self, *args, **kwargs):
        if not self.COGNITIVE_NVI_ANS_ID:
            self.COGNITIVE_NVI_ANS_ID = generate_unique_id(Cognitive_NVI_Answers_Dataset)
        with transaction.atomic():
            super(Cognitive_NVI_Answers_Dataset, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.COGNITIVE_NVI_ANS_ID)
    
class Cognitive_VI_Question_Dataset(models.Model):
    VI_QUESTION_ID = models.CharField(primary_key=True,max_length=10)
    QUESTION = models.TextField()
    OPTION1 = models.CharField(max_length=100)
    OPTION2 = models.CharField(max_length=100)
    OPTION3 = models.CharField(max_length=100)
    OPTION4 = models.CharField(max_length=100)
    OPTION5 = models.CharField(max_length=100)
    OPTION6 = models.CharField(max_length=100)
    OPTION7 = models.CharField(max_length=100)
    OPTION8 = models.CharField(max_length=100)
    ANSWER = models.CharField(max_length=100)

    def __str__(self):
        return str(self.VI_QUESTION_ID)

class Cognitive_VI_Answers_Dataset(models.Model):
    COGNITIVE_VI_ANS_ID = models.CharField(primary_key=True, editable=False, max_length=9)
    COGNITIVE_ASSESSMENT_ID = models.ForeignKey(Cognitive_Assessment, on_delete=models.CASCADE)
    VI_QUESTION_ID = models.ForeignKey(Cognitive_VI_Question_Dataset, on_delete=models.CASCADE)
    JOB_SEEKER_ANS = models.CharField(max_length=100)
    IS_CORRECT = models.BooleanField()

    def save(self, *args, **kwargs):
        if not self.COGNITIVE_VI_ANS_ID:
            self.COGNITIVE_VI_ANS_ID = generate_unique_id(Cognitive_VI_Answers_Dataset)
        with transaction.atomic():
            super(Cognitive_VI_Answers_Dataset, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.COGNITIVE_VI_ANS_ID)

class Cognitive_Assessment_Results(models.Model):
    COGNITIVE_ASSESSMENT_RESULT_ID = models.CharField(primary_key=True, editable=False, max_length=9)
    COGNITIVE_ASSESSMENT_ID = models.ForeignKey(Cognitive_Assessment, on_delete=models.CASCADE)
    COGNITIVE_VI_SCORE = models.IntegerField()
    COGNITIVE_NVI_SCORE = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.COGNITIVE_ASSESSMENT_RESULT_ID:
            self.COGNITIVE_ASSESSMENT_RESULT_ID = generate_unique_id(Cognitive_Assessment_Results)
        with transaction.atomic():
            super(Cognitive_Assessment_Results, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.COGNITIVE_ASSESSMENT_RESULT_ID)
    
class Technical_Assessment(models.Model):
    TECHNICAL_ASSESSMENT_ID = models.CharField(primary_key=True, editable=False, max_length=9)
    JOB_SEEKER_ASSESSMENT_ID = models.ForeignKey(Job_Seeker_Assessment, on_delete=models.CASCADE)
    TECHNICAL_ASSESSMENT_LEVEL = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.TECHNICAL_ASSESSMENT_ID:
            self.TECHNICAL_ASSESSMENT_ID = generate_unique_id(Technical_Assessment)
        with transaction.atomic():
            super(Technical_Assessment, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.TECHNICAL_ASSESSMENT_ID)

# creating model for technical question dataset
class Technical_Questions_Dataset(models.Model):
    TECH_ID = models.CharField(primary_key=True,max_length=10)
    JOB_POSITION = models.CharField(max_length=100)
    TEST_LEVEL = models.CharField(max_length=100)
    QUESTION = models.TextField()
    ANSWER = models.TextField()
    A = models.TextField()
    B = models.TextField()
    C = models.TextField()
    D = models.TextField()

    def __str__(self):
        # String representation of the model instance
        return self.TECH_ID

class Technical_Answers_Dataset(models.Model):
    TECH_ANS_ID = models.CharField(primary_key=True, editable=False, max_length=9)
    TECH_ID = models.ForeignKey(Technical_Questions_Dataset, on_delete=models.CASCADE)
    TECHNICAL_ASSESSMENT_ID = models.ForeignKey(Technical_Assessment, on_delete=models.CASCADE)
    JOB_SEEKER_ANS = models.CharField(max_length=100)
    IS_CORRECT = models.BooleanField()

    def save(self, *args, **kwargs):
        if not self.TECH_ANS_ID:
            self.TECH_ANS_ID = generate_unique_id(Technical_Answers_Dataset)
        with transaction.atomic():
            super(Technical_Answers_Dataset, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.TECH_ANS_ID)
    
class Technical_Assessment_Result(models.Model):
    TECHNICAL_ASSESSMENT_RESULT_ID = models.CharField(primary_key=True, editable=False, max_length=9)
    TECHNICAL_ASSESSMENT_ID = models.ForeignKey(Technical_Assessment, on_delete=models.CASCADE)
    SCORE = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.TECHNICAL_ASSESSMENT_RESULT_ID:
            self.TECHNICAL_ASSESSMENT_RESULT_ID = generate_unique_id(Technical_Assessment_Result)
        with transaction.atomic():
            super(Technical_Assessment_Result, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.TECHNICAL_ASSESSMENT_RESULT_ID)
