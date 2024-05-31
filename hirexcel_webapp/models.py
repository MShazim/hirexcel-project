from django.db import models

# creating model for disc questions datset
class Disc_Questions_Dataset(models.Model):
    DISC_PROFILE_ID = models.CharField(max_length=10, unique=True)
    QUESTION = models.TextField()
    A = models.CharField(max_length=100)
    B = models.CharField(max_length=100)
    C = models.CharField(max_length=100)
    D = models.CharField(max_length=100)

    def __str__(self):
        # String representation of the model instance
        return self.DISC_PROFILE_ID

# creating model for disc score calculation datset
class Disc_Score_Calculation_Dataset(models.Model):
    DISC_PROFILE_ID = models.CharField(max_length=10, unique=True)
    D = models.CharField(max_length=4)
    I = models.CharField(max_length=4)
    S = models.CharField(max_length=4)
    C = models.CharField(max_length=4)

    def __str__(self):
        # String representation of the model instance
        return self.DISC_PROFILE_ID

# creating model for NVI questions datset
class NVI_Questions_Dataset(models.Model):
    # A unique identifier for each image question
    IMAGE_ID = models.CharField(max_length=10, unique=True)
    
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
        return self.IMAGE_ID