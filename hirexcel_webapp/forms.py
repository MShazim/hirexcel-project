from django import forms
from .models import User_Information, Job_Seeker, Job_Seeker_Education, Job_Seeker_Work_Experience, Recruiter, Job_Posting

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserInformationForm(forms.ModelForm):
    class Meta:
        model = User_Information
        fields = ['FIRST_NAME', 'LAST_NAME', 'EMAIL', 'PASSWORD', 'CITY', 'COUNTRY', 'PHONE_NUMBER']

class JobSeekerForm(forms.ModelForm):
    class Meta:
        model = Job_Seeker
        fields = ['LINKEDIN_PROFILE_URL', 'GITHUB_PROFILE_URL', 'RESUME_UPLOAD']

class JobSeekerEducationForm(forms.ModelForm):
    class Meta:
        model = Job_Seeker_Education
        fields = ['INSTITUTION_NAME', 'PROGRAM', 'START_DATE', 'END_DATE', 'DEGREE']

class JobSeekerWorkExperienceForm(forms.ModelForm):
    class Meta:
        model = Job_Seeker_Work_Experience
        fields = ['COMPANY_NAME', 'DESIGNATION', 'START_DATE', 'END_DATE']

class RecruiterForm(forms.ModelForm):
    class Meta:
        model = Recruiter
        fields = ['COMPANY_NAME', 'COMPANY_WEBSITE', 'INDUSTRY', 'COMPANY_SIZE']


class JobPostingForm(forms.ModelForm):
    class Meta:
        model = Job_Posting
        fields = ['TITLE', 'DESCRIPTION', 'CITY', 'COUNTRY', 'JOB_TYPE', 'JOB_POSITION']