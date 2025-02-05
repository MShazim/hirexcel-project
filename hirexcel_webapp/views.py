from django.shortcuts import render , get_object_or_404 , redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.utils.timezone import now
# from .models import DISC_Questions_Dataset, Cognitive_NVI_Questions_Dataset, Technical_Questions_Dataset , Job_Position_Criteria ,User_Information, Job_Seeker, Job_Seeker_Education, Job_Seeker_Work_Experience , Recruiter, Job_Posting , Assessment , Job_Seeker_Assessment, Cognitive_Assessment , Cognitive_NVI_Answers_Dataset, Technical_Assessment, Technical_Answers_Dataset, BigFive_Assessment, BigFive_Questions_Dataset, Cognitive_VI_Question_Dataset
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

from .forms import UserInformationForm, JobSeekerForm, JobSeekerEducationForm, JobSeekerWorkExperienceForm , RecruiterForm , JobPostingForm
import random
from datetime import datetime
from datetime import timedelta
import json
import re
from django.views.decorators.csrf import csrf_exempt
# ---------------------------------[ for generating the evaluation summary using ChatGPT ]-----------------------------------------
from .utils.chatgpt_integration import ChatGPTIntegration
from django.conf import settings
# ---------------------------------[ end ]-----------------------------------------


# ---------------------------------[ START SCREEN ]-----------------------------------------
def start_screen(request):
    return render(request, './start-screen/start_screen.html')
# -------------------------------------[ ENDS ]---------------------------------------------


# ---------------------------------[ LOGIN/LOGOUT ]------------------------------------------

def jobseeker_login(request):
    if request.method == 'POST':
        email = request.POST['email-username']
        password = request.POST['password']

        try:
            user_info = User_Information.objects.get(EMAIL=email)
        except User_Information.DoesNotExist:
            user_info = None

        if user_info is not None and user_info.PASSWORD == password:
            # Check if the user is a job seeker
            try:
                job_seeker = Job_Seeker.objects.get(USER_ID=user_info)
                # Log in the user
                request.session['user_id'] = str(user_info.USER_ID)
                request.session['job_seeker_id'] = str(job_seeker.JOB_SEEKER_ID)
                return redirect('jobseeker_home')  # Redirect to jobseeker home page or dashboard
            except Job_Seeker.DoesNotExist:
                messages.error(request, "Couldn't find email, Please Sign Up")
        else:
            messages.error(request, 'Invalid email or password')

    return render(request, './login/job_seeker/jobseeker_login.html')

def recruiter_login(request):
    if request.method == 'POST':
        email = request.POST['email-username']
        password = request.POST['password']

        try:
            user_info = User_Information.objects.get(EMAIL=email)
        except User_Information.DoesNotExist:
            user_info = None

        if user_info is not None and user_info.PASSWORD == password:
            # Check if the user is a recruiter
            try:
                recruiter = Recruiter.objects.get(USER_ID=user_info)
                # Log in the user
                request.session['user_id'] = str(user_info.USER_ID)
                request.session['recruiter_id'] = str(recruiter.RECRUITER_ID)
                return redirect('recruiter_home')  # Redirect to recruiter home page or dashboard
            except Recruiter.DoesNotExist:
                messages.error(request, "Couldn't find email, Please Sign Up")
        else:
            messages.error(request, 'Invalid email or password')

    return render(request, './login/recruiter/recruiter_login.html')

def jobseeker_logout_view(request):
    # if 'user_id' in request.session:
    #     del request.session['user_id']
    request.session.flush()
    return redirect('jobseeker_login')  # Redirect to the login page or home page after logout

def recruiter_logout_view(request):
    # if 'user_id' in request.session:
    #     del request.session['user_id']
    request.session.flush()
    return redirect('recruiter_login')  # Redirect to the login page or home page after logout
# --------------------------------------[ ENDS ]---------------------------------------------

# ---------------------------------[ JOB SEEKER HOME ]---------------------------------------
# def jobseeker_home(request):
#     user_id = request.session.get('user_id')
#     if user_id:
#         user_info = User_Information.objects.get(USER_ID=user_id)
#         job_postings = Job_Posting.objects.all()  # Get all job postings
#         formatted_job_postings = [format_job_posting_data(job) for job in job_postings]
#         return render(request, 'home/job_seeker/index.html', {
#             'user_info': user_info,
#             'job_postings': formatted_job_postings
#         })
#     else:
#         return redirect('jobseeker_login')  # Redirect to login if not logged in

def jobseeker_home(request):
    user_id = request.session.get('user_id')
    if user_id:
        # Fetch the logged-in user's information
        user_info = User_Information.objects.get(USER_ID=user_id)
        
        # Get the associated Job Seeker
        job_seeker = Job_Seeker.objects.get(USER_ID=user_info)
        
        # Get all job postings
        job_postings = Job_Posting.objects.all()
        formatted_job_postings = [format_job_posting_data(job) for job in job_postings]

        # Fetch all Job Seeker Assessments for this job seeker
        applied_assessments = Job_Seeker_Assessment.objects.filter(JOB_SEEKER_ID=job_seeker)

        # Create a set of applied job IDs
        applied_job_ids = {assessment.JOB_POST_ID.JOB_POST_ID  for assessment in applied_assessments}

        print(applied_job_ids)

        # Render the template with the additional context for applied job IDs
        return render(request, 'home/job_seeker/index.html', {
            'user_info': user_info,
            'job_postings': formatted_job_postings,
            'applied_job_ids': applied_job_ids  # Pass the set of applied job IDs
        })
    else:
        return redirect('jobseeker_login')  # Redirect to login if not logged in

# --------------------------------------[ ENDS ]---------------------------------------------


# ---------------------------------[ RECRUITER HOME ]----------------------------------------
# def recruiter_home(request):
#     user_id = request.session.get('user_id')
#     if user_id:
#         user_info = User_Information.objects.get(USER_ID=user_id)
#         recruiter = Recruiter.objects.get(USER_ID=user_info)
#         job_postings = Job_Posting.objects.filter(RECRUITER_ID=recruiter)
#         formatted_job_postings = [format_job_posting_data(job) for job in job_postings]

#         return render(request, 'home/recruiter/index.html', {
#             'user_info': user_info,
#             'job_postings': formatted_job_postings
#         })
#     else:
#         return redirect('recruiter_login')  # Redirect to login if not logged in

def recruiter_home(request):
    user_id = request.session.get('user_id')
    if user_id:
        user_info = User_Information.objects.get(USER_ID=user_id)
        recruiter = Recruiter.objects.get(USER_ID=user_info)
        job_postings = Job_Posting.objects.all()  # Get all job postings
        formatted_job_postings = [format_job_posting_data(job) for job in job_postings]

        return render(request, 'home/recruiter/index.html', {
            'user_info': user_info,
            'job_postings': formatted_job_postings
        })
    else:
        return redirect('recruiter_login')  # Redirect to login if not logged in

# --------------------------------------[ ENDS ]---------------------------------------------

# ---------------------------------[ JOB POSTINGs RELATED Unchanged ]----------------------------------
def format_job_posting_data(job_posting):
    """Format job posting data for template rendering."""
    formatted_data = {
        'job_post_id': job_posting.JOB_POST_ID,
        'job_title': job_posting.TITLE,
        'company_name': job_posting.RECRUITER_ID.COMPANY_NAME,
        'job_position': job_posting.JOB_POSITION,
        'job_type': job_posting.JOB_TYPE,
        'city': job_posting.CITY,
        'country': job_posting.COUNTRY,
        'job_description': job_posting.DESCRIPTION,
        'required_qualifications': job_posting.REQUIRED_QUALIFICATIONS,
        'required_skills': job_posting.REQUIRED_SKILLS.split(', '),
        'experience_requirements': job_posting.EXPERIENCE_REQUIREMENTS,
        'personality_traits': job_posting.PERSONALITY_TRAITS.split(', '),
        'required_assessments': job_posting.REQUIRED_ASSESSMENTS.split(', '),
        'cog_weight': job_posting.COGNITIVE_WEIGHTAGE,
        'tech_weight': job_posting.TECHNICAL_WEIGHTAGE,
        'tech_assessment_level': job_posting.TECHNICAL_ASSESSMENT_LEVEL.split(', '),
        # 'test_criteria': job_posting.TEST_CRITERIA.split(', '),
    }
    return formatted_data

def post_job(request):
    user_id = request.session.get('user_id')
    user_info = User_Information.objects.get(USER_ID=user_id)
    if request.method == 'POST':
        try:
            print(request.POST)
            # Fetch recruiter and form fields as usual
            recruiter = Recruiter.objects.get(USER_ID__USER_ID=user_id)
            job_title = request.POST['jobTitle']
            city = request.POST['city']
            country = request.POST['country']
            job_type = request.POST['jobType']
            job_position = request.POST['jobPosition']
            job_description = request.POST['jobDescription']

            # Combine personality traits
            personality_traits = ', '.join(request.POST.getlist('personalityTraits'))

            # Fetch assessments
            # personality_assessments = ['DISC', 'BIG FIVE']  # Pre-selected personality assessments
            # cognitive_assessments = ['VERBAL', 'NON-VERBAL']  # Pre-selected cognitive assessments
            # required_assessments = ', '.join(personality_assessments + cognitive_assessments + [technical_assessments])

            # Combine into REQUIRED_ASSESSMENTS
            required_assessments = 'Personality Assessment, Cognitive Assessment, Technical Assessment'

            # Combine technical assessments
            technical_assessments = request.POST.getlist('technicalAssessment[]')
            technical_assessment_level = ', '.join(technical_assessments) 

            # Log for debugging
            print(f"Technical Assessments received: {technical_assessment_level}")

            # Other fields (e.g., qualifications, skills)
            required_qualifications = ', '.join(request.POST.getlist('requiredQualification'))
            experience_requirements = request.POST['experienceRequirements']

            # Parse the JSON returned by Tagify and extract the 'value' field
            raw_required_skills = request.POST['requiredSkills']
            skills_list = json.loads(raw_required_skills)
            required_skills = ', '.join([skill['value'] for skill in skills_list])

            # Fetching cognitive and technical weightage
            cognitive_weightage = request.POST['cognitiveWeightage']
            technical_weightage = request.POST['technicalWeightage']

            # Save the job posting
            job_posting = Job_Posting(
                TITLE=job_title,
                DESCRIPTION=job_description,
                RECRUITER_ID=recruiter,
                CITY=city,
                COUNTRY=country,
                JOB_TYPE=job_type,
                JOB_POSITION=job_position,
                PERSONALITY_TRAITS=personality_traits,
                REQUIRED_SKILLS=required_skills,
                REQUIRED_QUALIFICATIONS=required_qualifications,
                EXPERIENCE_REQUIREMENTS=experience_requirements,
                COGNITIVE_WEIGHTAGE=cognitive_weightage,
                TECHNICAL_WEIGHTAGE=technical_weightage,
                REQUIRED_ASSESSMENTS=required_assessments,
                TECHNICAL_ASSESSMENT_LEVEL=technical_assessment_level
            )
            job_posting.save()

            return redirect('recruiter_home')
        except KeyError as e:
            return HttpResponse(f"Missing key in POST data: {e}", status=400)
        except Recruiter.DoesNotExist:
            return HttpResponse("Recruiter not found", status=404)
        except Job_Position_Criteria.DoesNotExist:
            return HttpResponse("Job Position Criteria not found", status=404)

    job_positions = Job_Position_Criteria.objects.values_list('JOB_POSITION', flat=True).distinct()
    return render(request, './post_job/post_job.html', { 'user_info': user_info, 'job_positions': job_positions})

@csrf_exempt
def get_personality_traits(request):
    job_position = request.GET.get('job_position')
    print("Received job position:", job_position)  # Debugging

    if job_position:
        # Fetching the job position from the database
        criteria = Job_Position_Criteria.objects.filter(JOB_POSITION=job_position + " ")

        if criteria.exists():
            personality_traits_set = set()  # Use a set to avoid duplicates
            cognitive_weightage = None
            technical_weightage = None

            for criterion in criteria:
                # Add personality traits, cognitive skills, and emotional intelligence to the set
                if criterion.PERSONALITY_TRAITS and criterion.PERSONALITY_TRAITS.lower() != 'nan':
                    personality_traits_set.update(criterion.PERSONALITY_TRAITS.split(','))
                if criterion.COGNITIVE_SKILLS and criterion.COGNITIVE_SKILLS.lower() != 'nan':
                    personality_traits_set.update(criterion.COGNITIVE_SKILLS.split(','))
                if criterion.EMOTIONAL_INTELLIGENCE and criterion.EMOTIONAL_INTELLIGENCE.lower() != 'nan':
                    personality_traits_set.update(criterion.EMOTIONAL_INTELLIGENCE.split(','))

                # Fetch the weightage values (same for all criteria under the same job position)
                cognitive_weightage = criterion.COGNITIVE_WEIGHTAGE
                technical_weightage = criterion.TECHNICAL_WEIGHTAGE

                print("Received Personality Traits:", list(personality_traits_set))
                print("Received Cognitive Weightage:", cognitive_weightage)
                print("Received Technical Weightage:", technical_weightage)

            # Return the combined personality traits and weightages in the response
            return JsonResponse({
                'personality_traits': list(personality_traits_set),  # Convert set to list for JSON serialization
                'cognitive_weightage': cognitive_weightage,
                'technical_weightage': technical_weightage,
            })
        else:
            print("No matching criteria found for the job position")
            return JsonResponse({'personality_traits': [], 'cognitive_weightage': "N/A", 'technical_weightage': "N/A"})

    else:
        print("No job position provided")
        return JsonResponse({'personality_traits': [], 'cognitive_weightage': "N/A", 'technical_weightage': "N/A"})

#def apply_for_job(request, job_post_id):
    # if request.method == 'POST':
    #     # Hardcoded assessment categories
    #     assessment_categories = ["Cognitive_nvi", "Technical"]
    #     assessment_category_str = ', '.join(assessment_categories)

    #     # Create a single assessment record with combined categories
    #     assessment = Assessment.objects.create(
    #        ASSESSMENT_CATEGORY=assessment_category_str
    #     )

    #     # Store assessment_id and job_post_id in the session
    #     request.session['assessment_id'] = str(assessment.ASSESSMENT_ID)
    #     request.session['job_post_id'] = job_post_id

    #     # Redirect directly to disc quiz start
    #     return redirect('disc_quiz_start')
    # else:
    #     # If not a POST request, redirect back to jobseeker home
    #     return redirect('jobseeker_home')

#--------------------------------- NEW VIEW ADDED DURING TESTING---------------------------------
def apply_for_job(request, job_post_id):
    if request.method == 'POST':
        # Hardcoded assessment categories
        assessment_categories = ["Cognitive_nvi", "Technical"]
        assessment_category_str = ', '.join(assessment_categories)

        # Create an assessment without `ASSESSMENT_CATEGORY`
        assessment = Assessment.objects.create(
            JOB_POST_ID= Job_Posting.objects.get(JOB_POST_ID=job_post_id),
            COGNITIVE_WEIGHTAGE='40',
            TECHNICAL_WEIGHTAGE='60',
            TECHNICAL_ASSESSMENT_LEVEL='Basic'
        )

        # Store assessment_id and job_post_id in the session
        request.session['assessment_id'] = str(assessment.ASSESSMENT_ID)
        request.session['job_post_id'] = job_post_id

        # Redirect directly to disc quiz start
        return redirect('disc_quiz_start')
    else:
        # If not a POST request, redirect back to jobseeker home
        return redirect('jobseeker_home')


# ----------------------------[ CREATE ACCOUNT JS ]------------------------------------------
def job_seeker_create_account(request, step=1):
    step = int(step)  # Ensure step is always an integer
    context = {'step': step}
    
    if request.method == 'POST':
        # Step 1: Handle Personal Info
        if step == 1:
            form = UserInformationForm(request.POST)
            if form.is_valid():
                # Check if email already exists
                email = request.POST.get('EMAIL')
                existing_user = User_Information.objects.filter(EMAIL=email).first()
                if existing_user:
                    # Check if the existing user's ID is in the Job_Seeker table
                    if Recruiter.objects.filter(USER_ID=existing_user.USER_ID).exists():
                        messages.error(request, "This email exists in the Recruiter records. Please try a different email.")
                    else:
                        messages.error(request, "This email is already registered. Please try a different email.")
                    
                    context['form'] = form  # Re-render form with error
                else:
                    user = form.save()  # Save user info to DB
                    request.session['user_id'] = str(user.USER_ID)  # Store USER_ID in session
                    return redirect(reverse('job_seeker_create_account', args=[2]))  # Move to Step 2
            else:
                context['form'] = form

        # Step 2: Handle Education Info (Convert date fields to strings before saving in session)
        elif step == 2:
            form = JobSeekerEducationForm(request.POST)
            if form.is_valid():
                education_data = form.cleaned_data
                # Convert date fields to string format for JSON serialization
                education_data['START_DATE'] = education_data['START_DATE'].isoformat()
                education_data['END_DATE'] = education_data['END_DATE'].isoformat() if education_data['END_DATE'] else None
                request.session['education_data'] = education_data  # Store in session
                return redirect(reverse('job_seeker_create_account', args=[3]))  # Move to Step 3
            else:
                context['form'] = form

        # Step 3: Handle Work Experience (Convert date fields to strings)
        elif step == 3:
            form = JobSeekerWorkExperienceForm(request.POST)
            if form.is_valid():
                work_experience_data = form.cleaned_data
                # Convert date fields to string format for JSON serialization
                work_experience_data['START_DATE'] = work_experience_data['START_DATE'].isoformat()
                work_experience_data['END_DATE'] = work_experience_data['END_DATE'].isoformat() if work_experience_data['END_DATE'] else None
                request.session['work_experience_data'] = work_experience_data  # Store in session
                return redirect(reverse('job_seeker_create_account', args=[4]))  # Move to Step 4
            else:
                context['form'] = form

        # Step 4: Handle Job Seeker Info (Final POST and DB Save)
        elif step == 4:
            form = JobSeekerForm(request.POST, request.FILES)
            if form.is_valid():
                user_id = request.session.get('user_id')
                education_data = request.session.get('education_data')
                work_experience_data = request.session.get('work_experience_data')

                if user_id and education_data and work_experience_data:
                    user = User_Information.objects.get(USER_ID=user_id)

                    # Convert education and work experience date fields back to `datetime` objects
                    education_data['START_DATE'] = datetime.fromisoformat(education_data['START_DATE'])
                    education_data['END_DATE'] = datetime.fromisoformat(education_data['END_DATE']) if education_data['END_DATE'] else None
                    
                    work_experience_data['START_DATE'] = datetime.fromisoformat(work_experience_data['START_DATE'])
                    work_experience_data['END_DATE'] = datetime.fromisoformat(work_experience_data['END_DATE']) if work_experience_data['END_DATE'] else None

                    # Save Job Seeker data
                    job_seeker = form.save(commit=False)
                    job_seeker.USER_ID = user
                    job_seeker.save()

                    # Save Education data
                    education_form = JobSeekerEducationForm(education_data)
                    education = education_form.save(commit=False)
                    education.JOB_SEEKER_ID = job_seeker
                    education.save()

                    # Save Work Experience data
                    work_experience_form = JobSeekerWorkExperienceForm(work_experience_data)
                    work_experience = work_experience_form.save(commit=False)
                    work_experience.JOB_SEEKER_ID = job_seeker
                    work_experience.save()

                    request.session.flush()  # Clear session after successful save
                    return redirect('success_page')
                else:
                    context['error'] = "Missing required information. Please start from the beginning."
            else:
                context['form'] = form

    # Load appropriate form for each step
    if 'form' not in context:
        if step == 1:
            context['form'] = UserInformationForm()
        elif step == 2:
            context['form'] = JobSeekerEducationForm()
        elif step == 3:
            context['form'] = JobSeekerWorkExperienceForm()
        elif step == 4:
            context['form'] = JobSeekerForm()

    template_name = f"create_account/job_seeker/create_account_step{step}.html"
    return render(request, template_name, context)

def success_page(request):
    return render(request, 'create_account/job_seeker/success.html')
# ------------------------------------[ ENDS ]-----------------------------------------------

# ----------------------------[ CREATE ACCOUNT R ]--------------------------------------------
def recruiter_create_account(request, step=1):
    step = int(step)
    context = {'step': step}

    # Step 1: Handle Personal Info
    if request.method == 'POST':
        if step == 1:
            form = UserInformationForm(request.POST)
            if form.is_valid():
                # # Check if email already exists
                email = request.POST.get('EMAIL')
                # if User_Information.objects.filter(EMAIL=email).exists():
                #     messages.error(request, "This email is already registered. Please try a different email.")
                #     context['form'] = form  # Re-render form with error
                # else:
                #     user = form.save()  # Save recruiter personal info to DB
                #     request.session['user_id'] = str(user.USER_ID)  # Store recruiter ID in session
                #     return redirect('recruiter_create_account', step=2)  # Move to step 2 (company info)
                # Check if email already exists
                existing_user = User_Information.objects.filter(EMAIL=email).first()
                if existing_user:
                    # Check if the existing user's ID is in the Job_Seeker table
                    if Job_Seeker.objects.filter(USER_ID=existing_user.USER_ID).exists():
                        messages.error(request, "This email exists in the Job Seeker records. Please try a different email.")
                    else:
                        messages.error(request, "This email is already registered. Please try a different email.")
                    
                    context['form'] = form  # Re-render form with error
                else:
                    user = form.save()  # Save recruiter personal info to DB
                    request.session['user_id'] = str(user.USER_ID)  # Store recruiter ID in session
                    return redirect('recruiter_create_account', step=2)  # Move to step 2 (company info)
            else:
                context['form'] = form

        # Step 2: Handle Company Info
        elif step == 2:
            form = RecruiterForm(request.POST)
            if form.is_valid():
                user_id = request.session.get('user_id')

                if user_id:
                    user = User_Information.objects.get(USER_ID=user_id)

                    recruiter = form.save(commit=False)
                    recruiter.USER_ID = user
                    recruiter.save()

                    # Clear session after success
                    request.session.flush()
                    return redirect('recruiter_success_page')  # Redirect to success page
                else:
                    context['error'] = "Missing required information. Please start from the beginning."
            else:
                context['form'] = form

    # Load appropriate form for each step
    if 'form' not in context:
        if step == 1:
            context['form'] = UserInformationForm()
        elif step == 2:
            context['form'] = RecruiterForm()

    template_name = f"create_account/recruiter/create_account_step{step}.html"
    return render(request, template_name, context)

def recruiter_success_page(request):
    return render(request, 'create_account/recruiter/success.html')
# ------------------------------------[ ENDS ]-----------------------------------------------

#* ------------------------------------------------------------------------------------------
#* ---------------------------[ VIEW PROFILE SECTION ]---------------------------------------
#* ------------------------------------------------------------------------------------------

# --------------------------[ RECRUITER VIEW PROFILE ]---------------------------------------
def recruiter_view_profile(request):
    user_id = request.session.get('user_id')

    # Fetch User_Information and Recruiter data using the user_id
    user_information = User_Information.objects.get(USER_ID=user_id)
    recruiter_info = Recruiter.objects.get(USER_ID=user_information)
    job_postings = Job_Posting.objects.filter(RECRUITER_ID=recruiter_info)
    formatted_job_postings = [format_job_posting_data(job) for job in job_postings]

    # Fetch job seeker applications for this recruiter's job postings
    applied_job_seekers = []
    seen_assessment_ids = set() 

    for job_post in job_postings:
        # Get all assessments for the current job post
        assessments = Job_Seeker_Assessment.objects.filter(JOB_POST_ID=job_post.JOB_POST_ID)

        for assessment in assessments:
            # Check if the assessment has already been processed
            if assessment.ASSESSMENT_ID in seen_assessment_ids:
                continue  # Skip if this assessment ID is already processed

            # Add the assessment ID to the set of seen IDs
            seen_assessment_ids.add(assessment.ASSESSMENT_ID)

            # Get job seeker details
            job_seeker = Job_Seeker.objects.get(JOB_SEEKER_ID=assessment.JOB_SEEKER_ID)
            user_info = User_Information.objects.get(USER_ID=job_seeker.USER_ID)

            # Fetch the candidate status from the Evaluation_Summary table
            try:
                evaluation_summary = Evaluation_Summary.objects.get(ASSESSMENT_ID=assessment.ASSESSMENT_ID)
                candidate_status = evaluation_summary.CANDIDATE_STATUS
            except Evaluation_Summary.DoesNotExist:
                candidate_status = "Status Not Available"

            # Add the information to the list
            applied_job_seekers.append({
                'job_seeker_name': user_info.FIRST_NAME + ' ' + user_info.LAST_NAME,
                'job_seeker_email': user_info.EMAIL,
                'job_seeker_phone': user_info.PHONE_NUMBER,
                'job_title': job_post.TITLE,
                'job_position': job_post.JOB_POSITION,
                'job_type': job_post.JOB_TYPE,
                'assessment_id': assessment.ASSESSMENT_ID,
                'jobseeker_id': assessment.JOB_SEEKER_ID,
                'candidate_status': candidate_status
            })

    # Pass the data to the template context
    context = {
        'user_info': user_information,
        'recruiter_info': recruiter_info,
        'job_postings': formatted_job_postings,
        'applied_job_seekers': applied_job_seekers,
    }
    return render(request, 'view_profile/recruiter/view_profile.html', context)
# ------------------------------------[ ENDS ]-----------------------------------------------

# ---------------------[ JOBSEEKERS VIEW PROFILE BY RECRUITER ]-----------------------------
def view_jobseeker_profile_by_recruiter(request, job_seeker_id):
    # Get the logged-in recruiter's information from the session
    user_id = request.session.get('user_id')
    recruiter_user_info = User_Information.objects.get(USER_ID=user_id)

    # Fetch the job seeker information using the jobseeker_id parameter
    job_seeker = Job_Seeker.objects.get(JOB_SEEKER_ID=job_seeker_id)
    job_seeker_user_info = User_Information.objects.get(USER_ID=job_seeker.USER_ID)

    # Fetch job seeker education and work experience, allowing for multiple entries
    job_seeker_educations = Job_Seeker_Education.objects.get(JOB_SEEKER_ID=job_seeker)
    job_seeker_work_experiences = Job_Seeker_Work_Experience.objects.get(JOB_SEEKER_ID=job_seeker)

    # Prepare the context to include the logged-in recruiter's info and the job seeker's info
    context = {
        'user_info': recruiter_user_info,  # Logged-in recruiter's info for the navbar
        'job_seeker_info': job_seeker,  # Job seeker information to display on the profile
        'job_seeker_user_info': job_seeker_user_info,  # Job seeker's user information
        'educations': job_seeker_educations,  # Job seeker's education details
        'work_experiences': job_seeker_work_experiences,  # Job seeker's work experience details
    }

    return render(request, 'view_profile/recruiter/view_jobseeker_profile.html', context)
# ------------------------------------[ ENDS ]-----------------------------------------------

# --------------------------[ JOBSEEKER VIEW PROFILE ]---------------------------------------
def jobseeker_view_profile(request):
    user_id = request.session.get('user_id')

    # Fetch User_Information using the user_id
    user_information = User_Information.objects.get(USER_ID=user_id)

    # Fetch the Job_Seeker data using the user information
    job_seeker = Job_Seeker.objects.get(USER_ID=user_information)

    # Fetch Job Seeker Education and Work Experience, allowing for multiple entries
    job_seeker_educations = Job_Seeker_Education.objects.get(JOB_SEEKER_ID=job_seeker)
    job_seeker_work_experiences = Job_Seeker_Work_Experience.objects.get(JOB_SEEKER_ID=job_seeker)

     # Fetch applied jobs for this job seeker
    applied_jobs = []
    seen_assessment_ids = set()  # To keep track of processed Assessment_IDs

    job_seeker_assessments = Job_Seeker_Assessment.objects.filter(JOB_SEEKER_ID=job_seeker)

    for assessment in job_seeker_assessments:
        if assessment.ASSESSMENT_ID in seen_assessment_ids:
            continue  # Skip if this Assessment_ID has already been processed

        # Mark the Assessment_ID as processed
        seen_assessment_ids.add(assessment.ASSESSMENT_ID)

        # Get the associated Job Posting
        job_post = Job_Posting.objects.get(JOB_POST_ID=assessment.JOB_POST_ID)

        # Get the Recruiter information
        recruiter = Recruiter.objects.get(RECRUITER_ID=job_post.RECRUITER_ID)
        recruiter_user_info = User_Information.objects.get(USER_ID=recruiter.USER_ID)

        # Prepare the applied job data
        applied_jobs.append({
            'recruiter_name': recruiter_user_info.FIRST_NAME + ' ' + recruiter_user_info.LAST_NAME,
            'recruiter_email': recruiter_user_info.EMAIL,
            'company_name': recruiter.COMPANY_NAME,
            'job_title': job_post.TITLE,
            'job_position': job_post.JOB_POSITION,
            'job_type': job_post.JOB_TYPE,
            'assessment_id': assessment.ASSESSMENT_ID,
            'recruiter_id': job_post.RECRUITER_ID,
        })

    # Prepare the context for rendering the template
    context = {
        'user_info': user_information,
        'job_seeker_info': job_seeker,
        'educations': job_seeker_educations,
        'work_experiences': job_seeker_work_experiences,
        'applied_jobs': applied_jobs,
    }

    return render(request, 'view_profile/job_seeker/view_profile.html', context)
# ------------------------------------[ ENDS ]-----------------------------------------------

# ---------------------[ RECRUITERS VIEW PROFILE BY JOBSEEKER ]-----------------------------
def view_recruiter_profile_by_jobseeker(request, recruiter_id):
    
    user_id = request.session.get('user_id')
    user_information = User_Information.objects.get(USER_ID=user_id)

    # Fetch Recruiter information using recruiter_id
    recruiter = Recruiter.objects.get(RECRUITER_ID=recruiter_id)
    recruiter_user_info = User_Information.objects.get(USER_ID=recruiter.USER_ID)

    # Fetch job postings associated with the recruiter
    job_postings = Job_Posting.objects.filter(RECRUITER_ID=recruiter_id)
    formatted_job_postings = [format_job_posting_data(job) for job in job_postings]

    # Prepare the context for rendering the template
    context = {
        'user_info': user_information,
        'recruiter_user_info': recruiter_user_info,
        'recruiter_info': recruiter,
        'job_postings': formatted_job_postings,
    }

    return render(request, 'view_profile/job_seeker/view_recruiters_profile.html', context)
# ------------------------------------[ ENDS ]-----------------------------------------------


# ---------------------------[ GET REPORT DATA FOR THE MODAL ]-------------------------------
def get_report_data(request):
    assessment_id = request.GET.get('assessment_id')
    if not assessment_id:
        return JsonResponse({'error': 'Assessment ID is required'}, status=400)
    try:
        # Fetch the Evaluation_Summary based on the provided assessment_id
        evaluation_summary = Evaluation_Summary.objects.get(ASSESSMENT_ID=assessment_id)
        
        # Extract related information using the foreign keys
        user_info = evaluation_summary.USER_ID
        job_post = evaluation_summary.JOB_POST_ID
        personality_report = evaluation_summary.PERSONALITY_ASSESSMENT_REPORT_ID
        cognitive_assessment = evaluation_summary.COGNITIVE_ASSESSMENT_RESULT_ID
        technical_assessment = evaluation_summary.TECHNICAL_ASSESSMENT_RESULT_ID
        
        # Parse comma-separated values into lists
        personality_traits_list = [trait.strip() for trait in job_post.PERSONALITY_TRAITS.split(",")]
        technical_assessment_level_list = [level.strip() for level in job_post.TECHNICAL_ASSESSMENT_LEVEL.split(",")]
        disc_personality_trait_list = [trait.strip() for trait in personality_report.DISC_PERSONALITY_TRAIT.split(",")]
        bigf_openness_personality_list = [personality.strip() for personality in personality_report.BIGFIVE_OPENNESS_PERSONALITY.split(",")]
        bigf_concientiousness_personality_list = [personality.strip() for personality in personality_report.BIGFIVE_CONCIENTIOUSNESS_PERSONALITY.split(",")]
        bigf_extraversion_personality_list = [personality.strip() for personality in personality_report.BIGFIVE_EXTRAVERSION_PERSONALITY.split(",")]
        bigf_agreeableness_personality_list = [personality.strip() for personality in personality_report.BIGFIVE_AGREEABLENESS_PERSONALITY.split(",")]
        bigf_neuroticism_personality_list = [personality.strip() for personality in personality_report.BIGFIVE_NEUROTICISM_PERSONALITY.split(",")]
        disc_cognitive_abilities_list = [ability.strip() for ability in personality_report.DISC_COGNITIVE_ABILITY.split(",")]
        disc_tendencies_list = [tendency.strip() for tendency in personality_report.DISC_TENDENCIES.split(",")]
        disc_weaknesses_list = [weakness.strip() for weakness in personality_report.DISC_WEAKNESSES.split(",")]
        disc_behaviour_list = [behaviour.strip() for behaviour in personality_report.DISC_BEHAVIOUR.split(",")]
        disc_motivated_list = [motivate.strip() for motivate in personality_report.DISC_MOTIVATED_BY.split(",")]
        disc_emotional_list = [emotion.strip() for emotion in personality_report.DISC_EMOTIONAL_REGULATION.split(",")]
        
        # Determine cognitive and technical results
        cognitive_result = "Passed" if int(cognitive_assessment.COGNITIVE_SCORE_PERCENTAGE) >= int(job_post.COGNITIVE_WEIGHTAGE) else "Failed"
        technical_result = "Passed" if int(technical_assessment.TECH_SCORE_PERCENTAGE) >= int(job_post.TECHNICAL_WEIGHTAGE) else "Failed"
        
        # Parse optimal job matches
        optimal_job_matches_list = [match.strip() for match in re.split(r'\d+\.\s+', evaluation_summary.OPTIMAL_JOB_MATCHES) if match.strip()]
        candidate_status = "Recommended" if evaluation_summary.CANDIDATE_STATUS == "Recommended" else "Not Recommended"

        # Prepare data for JSON response
        report_data = {
            'user_info': {
                'first_name': user_info.FIRST_NAME,
                'last_name': user_info.LAST_NAME,
                'city': user_info.CITY,
                'country': user_info.COUNTRY,
                'phone_number': user_info.PHONE_NUMBER,
            },
            'job_post': {
                'title': job_post.TITLE,
                'job_type': job_post.JOB_TYPE,
                'job_position': job_post.JOB_POSITION,
                'cognitive_weightage': job_post.COGNITIVE_WEIGHTAGE,
                'technical_weightage': job_post.TECHNICAL_WEIGHTAGE,
            },
            'evaluation_summary': {
                'candidate_status': candidate_status,
                'profile_synopsis': evaluation_summary.PROFILE_SYNOPSIS,
            },
            'cognitive_result': cognitive_result,
            'technical_result': technical_result,
            'cognitive_assessment': {
                'cognitive_score_percentage': cognitive_assessment.COGNITIVE_SCORE_PERCENTAGE,
            },
            'technical_assessment': {
                'tech_score_percentage': technical_assessment.TECH_SCORE_PERCENTAGE,
            },
            'personality_report': personality_report.DISC_CATEGORY,
            'personality_traits_list': personality_traits_list,
            'technical_assessment_level_list': technical_assessment_level_list,
            'disc_personality_trait_list': disc_personality_trait_list,
            'bigf_openness_personality_list': bigf_openness_personality_list,
            'bigf_concientiousness_personality_list': bigf_concientiousness_personality_list,
            'bigf_extraversion_personality_list': bigf_extraversion_personality_list,
            'bigf_agreeableness_personality_list': bigf_agreeableness_personality_list,
            'bigf_neuroticism_personality_list': bigf_neuroticism_personality_list,
            'disc_cognitive_abilities_list': disc_cognitive_abilities_list,
            'disc_tendencies_list': disc_tendencies_list,
            'disc_weaknesses_list': disc_weaknesses_list,
            'disc_behaviour_list': disc_behaviour_list,
            'disc_motivated_list': disc_motivated_list,
            'disc_emotional_list': disc_emotional_list,
            'optimal_job_matches_list': optimal_job_matches_list,  # Make sure this is included in the backend data preparation
        }
        return JsonResponse({'report_data' : report_data})
    except (Job_Seeker_Assessment.DoesNotExist, Evaluation_Summary.DoesNotExist):
        return JsonResponse({'error': 'Report data not found'}, status=404)
# --------------------------------------[ ENDS ]---------------------------------------------

#* ------------------------------------------------------------------------------------------
#* -----------------------------------[ ENDS ]-----------------------------------------------
#* ------------------------------------------------------------------------------------------

# ----------------------------[ QUIZ START ]-------------------------------------------------
def quiz_start_screen(request):
    return render(request, './quiz/quiz_start_screen.html')


#* ------------------------------------------------------------------------------------------
#* ----------------------------[ DISC QUIZ INTEGRATED ]--------------------------------------
#* ------------------------------------------------------------------------------------------
# def disc_quiz_start_redirect(request):
#     if request.method == 'POST':
#         job_post_id = request.POST.get('job_post_id')
#         user_id = request.POST.get('user_id')

#         # Fetch the job posting details
#         job_posting = Job_Posting.objects.get(JOB_POST_ID=job_post_id)
#         cognitive_weightage = job_posting.COGNITIVE_WEIGHTAGE
#         technical_weightage = job_posting.TECHNICAL_WEIGHTAGE
#         technical_assessment_level = job_posting.TECHNICAL_ASSESSMENT_LEVEL

#         # Step 3: Create an Assessment record
#         assessment = Assessment.objects.create(
#             JOB_POST_ID=job_posting,
#             COGNITIVE_WEIGHTAGE=cognitive_weightage,
#             TECHNICAL_WEIGHTAGE=technical_weightage,
#             TECHNICAL_ASSESSMENT_LEVEL=technical_assessment_level,
#         )

#         # Save JOB_POST_ID in session
#         request.session['JOB_POST_ID'] = job_post_id
#         # Save ASSESSMENT_ID in session
#         request.session['ASSESSMENT_ID'] = assessment.ASSESSMENT_ID

#         # Fetch the job_seeker using user_id
#         job_seeker = Job_Seeker.objects.get(USER_ID=user_id)
#         job_seeker_id = job_seeker.JOB_SEEKER_ID

#         # Save JOB_SEEKER_ID in session
#         request.session['JOB_SEEKER_ID'] = job_seeker_id

#         # Fetch user's first name
#         user_info = User_Information.objects.get(USER_ID=user_id)
#         first_name = user_info.FIRST_NAME

#         # Calculate completion time
#         # completion_time = now() + timedelta(seconds=2040)

#         # Debugging: Print the completion_time to ensure it's a valid datetime
#         # print(f"Calculated Completion Time: {completion_time} (type: {type(completion_time)})")

#         # Step 4: Create a Job_Seeker_Assessment record
#         job_seeker_assessment = Job_Seeker_Assessment.objects.create(
#             JOB_SEEKER_ID=job_seeker,
#             JOB_POST_ID=job_posting,
#             ASSESSMENT_ID=assessment,
#             NAME=first_name,
#             ASSESSMENT_TYPE="Personality Assessment",
#             TOTAL_COMPLETION_TIME_REQUIRED="2040",  # Ensure this is a datetime object
#         )

#         # Step 5: Create a Personality_Assessment record
#         personality_assessment = Personality_Assessment.objects.create(
#             JOB_SEEKER_ASSESSMENT_ID=job_seeker_assessment
#         )

#         # Step 6: Create a DISC_Assessment record
#         disc_assessment = DISC_Assessment.objects.create(
#             PERSONALITY_ASSESSMENT_ID=personality_assessment,
#             DISC_COMPLETION_TIME_REQUIRED="720"
#         )

#         # Save JOB_SEEKER_ASSESSMENT_ID in session
#         request.session['JOB_SEEKER_ASSESSMENT_ID'] = job_seeker_assessment.JOB_SEEKER_ASSESSMENT_ID
#         # Save PERSONALITY_ASSESSMENT_ID in session
#         request.session['PERSONALITY_ASSESSMENT_ID'] = personality_assessment.PERSONALITY_ASSESSMENT_ID
#         # Save DISC_ASSESSMENT_ID in session
#         request.session['DISC_ASSESSMENT_ID'] = disc_assessment.DISC_ASSESSMENT_ID

#         # Step 7: Redirect to DISC Quiz start
#         return redirect('disc_quiz_start')

#     # Fallback if not a POST request
#     return redirect('jobseeker_home')

def disc_quiz_start_redirect(request):
    if request.method == 'POST':
        job_post_id = request.POST.get('job_post_id')
        user_id = request.POST.get('user_id')

        # Fetch the job posting details
        job_posting = Job_Posting.objects.get(JOB_POST_ID=job_post_id)
        cognitive_weightage = job_posting.COGNITIVE_WEIGHTAGE
        technical_weightage = job_posting.TECHNICAL_WEIGHTAGE
        technical_assessment_level = job_posting.TECHNICAL_ASSESSMENT_LEVEL

        # Step 3: Create an Assessment record
        assessment = Assessment.objects.create(
            JOB_POST_ID=job_posting,
            COGNITIVE_WEIGHTAGE=cognitive_weightage,
            TECHNICAL_WEIGHTAGE=technical_weightage,
            TECHNICAL_ASSESSMENT_LEVEL=technical_assessment_level,
        )

        # Save JOB_POST_ID in session
        request.session['JOB_POST_ID'] = job_post_id
        # Save ASSESSMENT_ID in session
        request.session['ASSESSMENT_ID'] = assessment.ASSESSMENT_ID

        # Fetch the job_seeker using user_id
        job_seeker = Job_Seeker.objects.get(USER_ID=user_id)
        job_seeker_id = job_seeker.JOB_SEEKER_ID

        # Save JOB_SEEKER_ID in session
        request.session['JOB_SEEKER_ID'] = job_seeker_id

        # Fetch user's first name
        user_info = User_Information.objects.get(USER_ID=user_id)
        first_name = user_info.FIRST_NAME

        # Calculate completion time
        # completion_time = now() + timedelta(seconds=2040)

        # Debugging: Print the completion_time to ensure it's a valid datetime
        # print(f"Calculated Completion Time: {completion_time} (type: {type(completion_time)})")

        # Step 4: Create a Job_Seeker_Assessment record
        job_seeker_assessment = Job_Seeker_Assessment.objects.create(
            JOB_SEEKER_ID=job_seeker,
            JOB_POST_ID=job_posting,
            ASSESSMENT_ID=assessment,
            NAME=first_name,
            ASSESSMENT_TYPE="Personality Assessment",
            TOTAL_COMPLETION_TIME_REQUIRED="2040",  # Ensure this is a datetime object
        )

        # Step 5: Create a Personality_Assessment record
        personality_assessment = Personality_Assessment.objects.create(
            JOB_SEEKER_ASSESSMENT_ID=job_seeker_assessment
        )

        # Step 6: Create a DISC_Assessment record
        disc_assessment = DISC_Assessment.objects.create(
            PERSONALITY_ASSESSMENT_ID=personality_assessment,
            DISC_COMPLETION_TIME_REQUIRED="720"
        )

        # Save JOB_SEEKER_ASSESSMENT_ID in session
        request.session['JOB_SEEKER_ASSESSMENT_ID'] = job_seeker_assessment.JOB_SEEKER_ASSESSMENT_ID
        # Save PERSONALITY_ASSESSMENT_ID in session
        request.session['PERSONALITY_ASSESSMENT_ID'] = personality_assessment.PERSONALITY_ASSESSMENT_ID
        # Save DISC_ASSESSMENT_ID in session
        request.session['DISC_ASSESSMENT_ID'] = disc_assessment.DISC_ASSESSMENT_ID

        # Step 7: Redirect to DISC Quiz start
        return redirect('disc_quiz_start')

    # Fallback if not a POST request
    return redirect('jobseeker_home')

def disc_quiz_start(request):
    # Redirect to the first question of DISC quiz
    first_question = DISC_Questions_Dataset.objects.first()
    if first_question:
        first_question_id = first_question.DISC_PROFILE_ID
        return redirect('disc_quiz', question_id=first_question_id)
    else:
        # Handle the case where there are no questions in the dataset
        return render(request, 'disc_quiz/no_questions.html')

def disc_quiz(request, question_id):
    # Fetch current question
    question = get_object_or_404(DISC_Questions_Dataset, DISC_PROFILE_ID=question_id)

    # All questions and next question logic...
    disc_assessment_id = request.session.get('DISC_ASSESSMENT_ID')  # Get DISC Assessment ID from session
    total_time = request.session.get('total_time', 0)  # Get total time spent on quiz

    if request.method == 'POST':
        selected_option = request.POST.get('selected_option')
        question_time = int(request.POST.get('question_time', 0))
        
        # Accumulate the time taken for this question
        total_time += question_time
        request.session['total_time'] = total_time  # Update the session with the new total time

        # If no option is selected (either by user or timer ran out), set it as 'nan'
        if not selected_option:
            selected_option = 'nan'

        # Fetch score calculation entry
        score_calculation_entry = get_object_or_404(DISC_Score_Calculation_Dataset, DISC_PROFILE_SCORE_ID=question.DISC_PROFILE_ID)

        # Determine DISC profile
        if selected_option == score_calculation_entry.D:
            disc_profile = 'D'
        elif selected_option == score_calculation_entry.I:
            disc_profile = 'I'
        elif selected_option == score_calculation_entry.S:
            disc_profile = 'S'
        elif selected_option == score_calculation_entry.C:
            disc_profile = 'C'
        else:
            disc_profile = 'nan'  # Set 'nan' for unselected or unknown options

        # Save the answer
        DISC_Assessment_Answer.objects.create(
            DISC_ASSESSMENT_ID_id=disc_assessment_id,
            DISC_PROFILE_ID=question,
            DISC_PROFILE_SCORE_ID=score_calculation_entry,
            JOB_SEEKER_ANS=selected_option,
            DISC_PROFILE=disc_profile
        )

        # Check if it's the last question
        next_question = DISC_Questions_Dataset.objects.filter(DISC_PROFILE_ID__gt=question_id).order_by('DISC_PROFILE_ID').first()
        if next_question:
            # Redirect to next question
            return redirect('disc_quiz', question_id=next_question.DISC_PROFILE_ID)
        else:
            # If last question, calculate total score and redirect to completion
            return redirect('disc_completion')

    # Get all questions to calculate the question number
    all_questions = list(DISC_Questions_Dataset.objects.order_by('DISC_PROFILE_ID'))
    total_questions = len(all_questions)
    current_question_number = all_questions.index(question) + 1

    # Calculate progress percentage
    progress_percentage = (current_question_number / total_questions) * 100

    context = {
        'question': question,
        'next_question_id': None if current_question_number == total_questions else all_questions[current_question_number].DISC_PROFILE_ID,
        'total_questions': total_questions,
        'current_question_number': current_question_number,
        'progress_percentage': progress_percentage
    }

    return render(request, 'disc_quiz/disc_quiz.html', context)

def disc_completion(request):
    disc_assessment_id = request.session.get('DISC_ASSESSMENT_ID')
    total_time = request.session.get('total_time', 0)  # Get total time in seconds

    # If the total time is zero, prevent further processing
    if total_time == 0:
        # Render a message or simply redirect to prevent duplicate entry
        return render(request, 'disc_quiz/disc_completion.html', {
            'message': "DISC Assessment already completed."
        })

    # Calculate scores
    answers = DISC_Assessment_Answer.objects.filter(DISC_ASSESSMENT_ID=disc_assessment_id)
    dominance_score = answers.filter(DISC_PROFILE='D').count()
    influencing_score = answers.filter(DISC_PROFILE='I').count()
    steadiness_score = answers.filter(DISC_PROFILE='S').count()
    concientiousness_score = answers.filter(DISC_PROFILE='C').count()

    disc_scores = {
        'Dominance': dominance_score,
        'Influencing': influencing_score,
        'Steadiness': steadiness_score,
        'Conscientiousness': concientiousness_score
    }
    disc_category = max(disc_scores, key=disc_scores.get)

    # Store total time as a string in seconds
    total_time_str = str(total_time)

    # Populate DISC_Assessment_Result table
    DISC_Assessment_Result.objects.create(
        DISC_ASSESSMENT_ID_id=disc_assessment_id,
        DISC_CATEGORY=disc_category,
        DOMINANCE_SCORE=dominance_score,
        INFLUENCING_SCORE=influencing_score,
        STEADINESS_SCORE=steadiness_score,
        CONCIENTIOUSNESS_SCORE=concientiousness_score,
        TOTAL_DISC_COMPLETION_TIME=total_time_str  # Save total time in seconds as string
    )

    # Delete the total time from session
    if 'total_time' in request.session:
        del request.session['total_time']

    # Redirect to the disc_completion.html template
    return render(request, 'disc_quiz/disc_completion.html')
#* ------------------------------------------------------------------------------------------
#* -----------------------------------[ ENDS ]-----------------------------------------------
#* ------------------------------------------------------------------------------------------

#* ------------------------------------------------------------------------------------------
#* ------------------------------[ BIG FIVE QUIZ INTEGRATED ]--------------------------------
#* ------------------------------------------------------------------------------------------
def big_five_quiz_start_redirect(request):
    # Retrieve the Personality Assessment ID from session
    personality_assessment_id = request.session.get('PERSONALITY_ASSESSMENT_ID')

    # Ensure we handle POST method for creating the BigFive_Assessment entry
    if request.method == 'POST':
        if personality_assessment_id:
            # Create the BigFive_Assessment entry
            big_five_assessment = BigFive_Assessment.objects.create(
                PERSONALITY_ASSESSMENT_ID_id=personality_assessment_id,
                BIGFIVE_COMPLETION_TIME_REQUIRED='1320'  # Static value as specified
            )
            # Store the BIGFIVE_ASSESSMENT_ID in the session
            request.session['BIGFIVE_ASSESSMENT_ID'] = big_five_assessment.BIGFIVE_ASSESSMENT_ID

        # Redirect to the first question of the quiz
        return redirect('big_five_quiz_start')

    # If not a POST request, render a confirmation form (for demonstration)
    return render(request, 'big_five_quiz/confirm_start.html')

def big_five_quiz_start(request):
    # Get all questions and sort them properly based on the numeric part of the dimension ID
    all_questions = list(BigFive_Questions_Dataset.objects.all())
    sorted_questions = sorted(
        all_questions,
        key=lambda q: int(re.search(r'(\d+)$', q.DIMENSION_ID).group())
    )

    # Redirect to the first sorted question
    if sorted_questions:
        first_question_id = sorted_questions[0].DIMENSION_ID
        return redirect('big_five_quiz', question_id=first_question_id)
    else:
        # Handle the case where there are no questions in the dataset
        return render(request, 'big_five_quiz/no_questions.html')

def big_five_quiz(request, question_id):
    # Get the question based on the current question ID
    question = get_object_or_404(BigFive_Questions_Dataset, DIMENSION_ID=question_id)

    # Extract all questions and sort them by the numeric part of DIMENSION_ID
    all_questions = list(BigFive_Questions_Dataset.objects.all())
    sorted_questions = sorted(
        all_questions,
        key=lambda q: int(re.search(r'(\d+)$', q.DIMENSION_ID).group())
    )

    total_questions = len(sorted_questions)
    current_question_number = sorted_questions.index(question) + 1

    # Calculate progress percentage
    progress_percentage = (current_question_number / total_questions) * 100

    # Get the next question ID
    next_question_id = None
    try:
        next_question_id = sorted_questions[current_question_number].DIMENSION_ID
    except IndexError:
        next_question_id = None  # Last question

    # Get BIGFIVE_ASSESSMENT_ID from session
    bigfive_assessment_id = request.session.get('BIGFIVE_ASSESSMENT_ID')
    total_time = request.session.get('total_bigfive_time', 0)  # Get total time spent

    if request.method == 'POST':
        # Get user's answer
        selected_option = request.POST.get('selected_option', '0')  # Defaults to '0' if no option is selected
        question_time = int(request.POST.get('question_time', 0))  # Time taken for the question in seconds

        # Add time taken for the current question to the total time
        total_time += question_time
        request.session['total_bigfive_time'] = total_time  # Update session with the new total time

        # Save the answer to the BigFive_Assessment_Answers table
        BigFive_Assessment_Answers.objects.create(
            BIGFIVE_ASSESSMENT_ID_id=bigfive_assessment_id,
            DIMENSION_ID=question,
            DIMENSION=question.DIMENSION,
            JOB_SEEKER_ANS=selected_option
        )

        # Redirect to next question or completion page
        if next_question_id:
            return redirect('big_five_quiz', question_id=next_question_id)
        else:
            # Redirect to the completion screen
            return redirect('big_five_completion')

    context = {
        'question': question,
        'next_question_id': next_question_id,
        'total_questions': total_questions,
        'current_question_number': current_question_number,
        'progress_percentage': progress_percentage
    }
    return render(request, 'big_five_quiz/big_five_quiz.html', context)

def big_five_completion(request):
    bigfive_assessment_id = request.session.get('BIGFIVE_ASSESSMENT_ID')
    disc_assessment_id = request.session.get('DISC_ASSESSMENT_ID')
    personality_assessment_id = request.session.get('PERSONALITY_ASSESSMENT_ID')
    job_seeker_assessment_id = request.session.get('JOB_SEEKER_ASSESSMENT_ID')
    total_time = request.session.get('total_bigfive_time', 0)  # Get total time in seconds


    # If the total time is zero, prevent further processing
    if total_time == 0:
        # Render a message or simply redirect to prevent duplicate entry
        return render(request, 'big_five_quiz/bigfive_completion.html', {
            'message': "Assessment already completed."
        })

    # Calculate scores
    answers = BigFive_Assessment_Answers.objects.filter(BIGFIVE_ASSESSMENT_ID=bigfive_assessment_id)
    
    # Sum scores based on dimensions
    openness_score = sum(int(answer.JOB_SEEKER_ANS) for answer in answers.filter(DIMENSION='Openness'))
    conscientiousness_score = sum(int(answer.JOB_SEEKER_ANS) for answer in answers.filter(DIMENSION='Conscientiousness'))
    extraversion_score = sum(int(answer.JOB_SEEKER_ANS) for answer in answers.filter(DIMENSION='Extraversion'))
    agreeableness_score = sum(int(answer.JOB_SEEKER_ANS) for answer in answers.filter(DIMENSION='Agreeableness'))
    neuroticism_score = sum(int(answer.JOB_SEEKER_ANS) for answer in answers.filter(DIMENSION='Neuroticism'))

    # Calculate dimension with the highest score
    dimension_scores = {
        'Openness': openness_score,
        'Conscientiousness': conscientiousness_score,
        'Extraversion': extraversion_score,
        'Agreeableness': agreeableness_score,
        'Neuroticism': neuroticism_score,
    }
    highest_dimension = max(dimension_scores, key=dimension_scores.get)

    # Store total time as a string in seconds
    total_time_str = str(total_time)

    # Populate BigFive_Assessment_Result table
    BigFive_Assessment_Result.objects.create(
        BIGFIVE_ASSESSMENT_ID_id=bigfive_assessment_id,
        DIMENSION=highest_dimension,
        OPENNESS_SCORE=openness_score,
        CONCIENTIOUSNESS_SCORE=conscientiousness_score,
        EXTRAVERSION_SCORE=extraversion_score,
        AGREEABLENESS_SCORE=agreeableness_score,
        NEUROTICISM_SCORE=neuroticism_score,
        TOTAL_BIGFIVE_COMPLETION_TIME=total_time_str  # Save total time in seconds as string
    )

    # Get DISC category from DISC_Assessment_Result
    disc_result = DISC_Assessment_Result.objects.get(DISC_ASSESSMENT_ID=disc_assessment_id)
    disc_category = disc_result.DISC_CATEGORY.strip()

    if disc_category == "Dominance":
        disc_category = "Dominance "
    elif disc_category == "Influencing":
        disc_category = "Influencing"
    elif disc_category == "Steadiness":
        disc_category = "Steadiness "
    elif disc_category == "Conscientiousness":
        disc_category = "Conscientiousness "

    print(f"----------------Disc category---------------: {disc_category}")

    # Print all DISC categories in the database for debugging
    all_disc_categories = DISC_Characteristics_Dataset.objects.values_list('DISC_CATEGORY', flat=True)
    # print(f"All DISC categories in dataset: {list(all_disc_categories)}")

    # Find matching DISC characteristics
    try:
        disc_characteristics = DISC_Characteristics_Dataset.objects.get(DISC_CATEGORY__iexact=disc_category)
        # print(f"-------------Fetched DISC characteristics----------------: {disc_characteristics}")
    except DISC_Characteristics_Dataset.DoesNotExist:
        # Handle if no match found
        disc_characteristics = None
        # print(f"-------------NOT FETCHED DISC characteristics----------------: {disc_characteristics}")

    # Extract DISC details
    disc_personality_trait = disc_characteristics.PERSONALITY_TRAIT if disc_characteristics else "Unknown"
    disc_cognitive_ability = disc_characteristics.COGNITIVE_ABILITY if disc_characteristics else "Not available"
    disc_emotional_regulation = disc_characteristics.EMOTIONAL_REGULATION if disc_characteristics else "Not available"
    disc_tendencies = disc_characteristics.TENDENCIES if disc_characteristics else "Not available"
    disc_weaknesses = disc_characteristics.WEAKNESSES if disc_characteristics else "Not available"
    disc_behaviour = disc_characteristics.BEHAVIOUR if disc_characteristics else "Not available"
    disc_motivated_by = disc_characteristics.MOTIVATED_BY if disc_characteristics else "Not available"

    # print("---------- DIMENSION PRINT-----------")
    # print(list(BigFive_Characteristics_Dataset.objects.values_list('DIMENSION', flat=True)))
    # print("----------------------------------")

    # Function to get BigFive details based on score and dimension
    def get_bigfive_characteristics(dimension, score):

        if dimension == "Openness":
            dimension = "Openness "
        elif dimension == "Conscientiousness":
            dimension = "Conscientiousness "
        elif dimension == "Agreeableness":
            dimension = "Agreeableness "


        bigfive_characteristic = BigFive_Characteristics_Dataset.objects.filter(
            DIMENSION__iexact=dimension
        ).order_by('RANGE')

        # print(f"Fetching details for Dimension: {dimension}, Score: {score}")

        # Print all ranges for the current dimension
        # for characteristic in bigfive_characteristic:
        #     print(f"Available range for {dimension}: {characteristic.RANGE}")

        for characteristic in bigfive_characteristic:
            range_parts = list(map(int, characteristic.RANGE.strip().replace(' ', '').split('-')))
            # print(f"Checking dimension: {dimension}, Score: {score}, Range: {range_parts}")

            if range_parts[0] <= score <= range_parts[1]:
                # print(f"Match found for Dimension: {dimension}, Score: {score}, Range: {range_parts}")
                return {
                    "category": characteristic.CATEGORY,
                    "personality": characteristic.PERSONALITY,
                    "description": characteristic.DESCRIPTION,
                    "workplace_behaviour": characteristic.WORKPLACE_BEHAVIOUR
                }

        # print(f"No match found for Dimension: {dimension}, Score: {score}")
        return {
            "category": "Unknown",
            "personality": "Not available",
            "description": "Not available",
            "workplace_behaviour": "Not available"
        }


    # Fetch characteristics for each Big Five dimension
    openness_details = get_bigfive_characteristics('Openness', openness_score)
    conscientiousness_details = get_bigfive_characteristics('Conscientiousness', conscientiousness_score)
    extraversion_details = get_bigfive_characteristics('Extraversion', extraversion_score)
    agreeableness_details = get_bigfive_characteristics('Agreeableness', agreeableness_score)
    neuroticism_details = get_bigfive_characteristics('Neuroticism', neuroticism_score)

    # Populate Personality_Assessment_Report table
    Personality_Assessment_Report.objects.create(
        PERSONALITY_ASSESSMENT_ID_id=personality_assessment_id,
        JOB_SEEKER_ASSESSMENT_ID_id=job_seeker_assessment_id,
        BIGFIVE_ASSESSMENT_ID_id=bigfive_assessment_id,
        DISC_ASSESSMENT_ID_id=disc_assessment_id,
        DISC_CATEGORY=disc_category,
        DISC_PERSONALITY_TRAIT=disc_personality_trait,
        DISC_COGNITIVE_ABILITY=disc_cognitive_ability,
        DISC_EMOTIONAL_REGULATION=disc_emotional_regulation,
        DISC_TENDENCIES=disc_tendencies,
        DISC_WEAKNESSES=disc_weaknesses,
        DISC_BEHAVIOUR=disc_behaviour,
        DISC_MOTIVATED_BY=disc_motivated_by,
        BIGFIVE_OPENNESS_SCORE=openness_score,
        BIGFIVE_OPENNESS_CATEGORY=openness_details["category"],
        BIGFIVE_OPENNESS_PERSONALITY=openness_details["personality"],
        BIGFIVE_OPENNESS_DESCRIPTION=openness_details["description"],
        BIGFIVE_OPENNESS_WORKPLACE_BEHAVIOUR=openness_details["workplace_behaviour"],
        BIGFIVE_CONCIENTIOUSNESS_SCORE=conscientiousness_score,
        BIGFIVE_CONCIENTIOUSNESS_CATEGORY=conscientiousness_details["category"],
        BIGFIVE_CONCIENTIOUSNESS_PERSONALITY=conscientiousness_details["personality"],
        BIGFIVE_CONCIENTIOUSNESS_DESCRIPTION=conscientiousness_details["description"],
        BIGFIVE_CONCIENTIOUSNESS_WORKPLACE_BEHAVIOUR=conscientiousness_details["workplace_behaviour"],
        BIGFIVE_EXTRAVERSION_SCORE=extraversion_score,
        BIGFIVE_EXTRAVERSION_CATEGORY=extraversion_details["category"],
        BIGFIVE_EXTRAVERSION_PERSONALITY=extraversion_details["personality"],
        BIGFIVE_EXTRAVERSION_DESCRIPTION=extraversion_details["description"],
        BIGFIVE_EXTRAVERSION_WORKPLACE_BEHAVIOUR=extraversion_details["workplace_behaviour"],
        BIGFIVE_AGREEABLENESS_SCORE=agreeableness_score,
        BIGFIVE_AGREEABLENESS_CATEGORY=agreeableness_details["category"],
        BIGFIVE_AGREEABLENESS_PERSONALITY=agreeableness_details["personality"],
        BIGFIVE_AGREEABLENESS_DESCRIPTION=agreeableness_details["description"],
        BIGFIVE_AGREEABLENESS_WORKPLACE_BEHAVIOUR=agreeableness_details["workplace_behaviour"],
        BIGFIVE_NEUROTICISM_SCORE=neuroticism_score,
        BIGFIVE_NEUROTICISM_CATEGORY=neuroticism_details["category"],
        BIGFIVE_NEUROTICISM_PERSONALITY=neuroticism_details["personality"],
        BIGFIVE_NEUROTICISM_DESCRIPTION=neuroticism_details["description"],
        BIGFIVE_NEUROTICISM_WORKPLACE_BEHAVIOUR=neuroticism_details["workplace_behaviour"]
    )

    # Delete the total time from session after completion
    if 'total_bigfive_time' in request.session:
        del request.session['total_bigfive_time']

    # Render the completion screen
    return render(request, 'big_five_quiz/bigfive_completion.html')

#* ------------------------------------------------------------------------------------------
#* --------------------------------------[ ENDS ]--------------------------------------------
#* ------------------------------------------------------------------------------------------


#* ------------------------------------------------------------------------------------------
#* -----------------------------[ VERBAL QUIZ INTEGRATED]------------------------------------
#* ------------------------------------------------------------------------------------------
def verbal_quiz_start_redirect(request):
    # Ensure this view is only accessed via a POST request
    if request.method == 'POST':
        # Step 1: Remove the old JOB_SEEKER_ASSESSMENT_ID from session if exists
        if 'JOB_SEEKER_ASSESSMENT_ID' in request.session:
            del request.session['JOB_SEEKER_ASSESSMENT_ID']
        
        # Retrieve required values from session
        job_seeker_id = request.session.get('JOB_SEEKER_ID')
        job_post_id = request.session.get('JOB_POST_ID')
        assessment_id = request.session.get('ASSESSMENT_ID')

        # Fetch the `Job_Seeker` instance using `job_seeker_id`
        job_seeker = Job_Seeker.objects.get(JOB_SEEKER_ID=job_seeker_id)

        # Fetch user's first name from `User_Information`
        user_info = User_Information.objects.get(USER_ID=job_seeker.USER_ID)
        first_name = user_info.FIRST_NAME

        # Create a new `Job_Seeker_Assessment` record
        job_seeker_assessment = Job_Seeker_Assessment.objects.create(
            JOB_SEEKER_ID=job_seeker,
            JOB_POST_ID_id=job_post_id,
            ASSESSMENT_ID_id=assessment_id,
            NAME=first_name,
            ASSESSMENT_TYPE="Cognitive Assessment",
            TOTAL_COMPLETION_TIME_REQUIRED="1800"  # Static value as specified
        )
        
        # Save the newly created `JOB_SEEKER_ASSESSMENT_ID` in session
        request.session['JOB_SEEKER_ASSESSMENT_ID'] = job_seeker_assessment.JOB_SEEKER_ASSESSMENT_ID
        
        # Step 2: Populate the `Cognitive_Assessment` table
        cognitive_assessment = Cognitive_Assessment.objects.create(
            JOB_SEEKER_ASSESSMENT_ID=job_seeker_assessment,
            COGNITIVE_COMPLETION_TIME_REQUIRED="1800"  # Static value as specified
        )
        
        # Save the `COGNITIVE_ASSESSMENT_ID` in session for further use
        request.session['COGNITIVE_ASSESSMENT_ID'] = cognitive_assessment.COGNITIVE_ASSESSMENT_ID
        
        # Step 3: Redirect to the start of the verbal quiz
        return redirect('verbal_quiz_start')
    
    # Fallback in case of non-POST request
    return redirect('jobseeker_home')

def verbal_quiz_start(request):
    # Fetch 15 random questions from the Cognitive_VI_Question_Dataset
    if 'verbal_selected_questions' not in request.session:
        question_ids = list(Cognitive_VI_Question_Dataset.objects.values_list('VI_QUESTION_ID', flat=True))
        selected_questions = random.sample(question_ids, 15) if len(question_ids) >= 15 else question_ids
        request.session['verbal_selected_questions'] = selected_questions
        print(f"Selected Verbal Questions: {selected_questions}")

    # Start with the first question (index 0)
    return redirect('verbal_quiz', question_index=0)

def verbal_quiz(request, question_index=0):
    # Fetch the selected questions from the session
    selected_questions = request.session.get('verbal_selected_questions', [])
    
    if not selected_questions:
        return redirect('verbal_quiz_start')

    # Get the question ID and fetch the question details
    question_id = selected_questions[question_index]
    question = get_object_or_404(Cognitive_VI_Question_Dataset, VI_QUESTION_ID=question_id)

    # Get the next question index
    next_question_index = question_index + 1 if question_index < len(selected_questions) - 1 else None

    cognitive_assessment_id = request.session.get('COGNITIVE_ASSESSMENT_ID')

    if request.method == 'POST':
        # Capture the user's selected option or "nan" if not selected
        selected_option = request.POST.get('option', 'nan')

        # Check if the selected option is correct
        is_correct = selected_option == question.ANSWER

        # Save the answer to Cognitive_VI_Answers_Dataset
        Cognitive_VI_Answers_Dataset.objects.create(
            COGNITIVE_ASSESSMENT_ID_id=cognitive_assessment_id,
            VI_QUESTION_ID=question,
            JOB_SEEKER_ANS=selected_option,
            IS_CORRECT=is_correct
        )

        # Save the time taken for the question
        time_taken = request.POST.get('time_taken', 60)  # Default to 60 if not present
        cog_vi_time = request.session.get('cog_vi_time', 0) + int(time_taken)
        request.session['cog_vi_time'] = cog_vi_time
        
        # Debugging: Print the time taken and cumulative time
        print(f"----Time taken for question {question_index}: {time_taken} seconds---------------")
        print(f"----------Cumulative time so far: {cog_vi_time} seconds--------------------------")

        # Redirect to the next question or completion if finished
        if next_question_index is not None:
            return redirect('verbal_quiz', question_index=next_question_index)
        else:
            # Redirect to the verbal quiz completion page
            return redirect('verbal_quiz_completion')

    # Prepare the options from the question object
    options = [
        question.A.strip(), question.B.strip(), question.C.strip(), question.D.strip(),
        question.E.strip(), question.F.strip(), question.G.strip(), question.H.strip()
    ]

    # Filter out any empty, "nan", or "none" options
    options = [option for option in options if option and option.lower() not in ["none", "nan"]]

    current_question_number = question_index + 1
    total_questions = len(selected_questions)
    
    # Calculate progress percentage
    progress_percentage = (current_question_number / total_questions) * 100

    context = {
        'question': question,
        'next_question_index': next_question_index,
        'total_questions': total_questions,
        'current_question_number': current_question_number,
        'options': options,
        'progress_percentage': progress_percentage
    }

    return render(request, 'verbal_quiz/verbal_quiz.html', context)

def verbal_quiz_completion(request):

    # Reset the cumulative time for the verbal quiz
    # if 'cog_vi_time' in request.session:
    #     del request.session['cog_vi_time']

    cog_vi_time = request.session['cog_vi_time']
    print(f"----------COGNITIVE VERBAL ASSESSMENT TIME IS : {cog_vi_time} --------------")

    return render(request, 'verbal_quiz/verbal_quiz_completion.html')
#* ------------------------------------------------------------------------------------------
#* --------------------------------------[ ENDS ]--------------------------------------------
#* ------------------------------------------------------------------------------------------

#* ------------------------------------------------------------------------------------------
#* ----------------------------[ NON VERBAL QUIZ INTEGRATED ]--------------------------------
#* ------------------------------------------------------------------------------------------
def non_verbal_quiz_start_redirect(request):
    return redirect('non_verbal_quiz_start')

def non_verbal_quiz_start(request):
    if 'selected_questions' not in request.session:
        question_ids = list(Cognitive_NVI_Questions_Dataset.objects.values_list('NVI_IMAGE_QUESTION_ID', flat=True))
        selected_questions = random.sample(question_ids, 15) if len(question_ids) >= 15 else question_ids
        request.session['selected_questions'] = selected_questions
        print(selected_questions)
    return redirect('non_verbal_quiz', question_index=0)


def non_verbal_quiz(request, question_index=0):
    selected_questions = request.session.get('selected_questions', [])
    
    if not selected_questions:
        return redirect('non_verbal_quiz_start')

    question_id = selected_questions[question_index]
    question = get_object_or_404(Cognitive_NVI_Questions_Dataset, NVI_IMAGE_QUESTION_ID=question_id)
    next_question_index = question_index + 1 if question_index < len(selected_questions) - 1 else None
    cognitive_assessment_id = request.session.get('COGNITIVE_ASSESSMENT_ID')

    if request.method == 'POST':
        # Capture user's answer or "nan" if not answered within time
        selected_option_index = request.POST.get('option', 'nan')

        # Map the user's option (1 to 8) to corresponding answer (A to H)
        option_map = {
            '1': question.OPTION1,
            '2': question.OPTION2,
            '3': question.OPTION3,
            '4': question.OPTION4,
            '5': question.OPTION5,
            '6': question.OPTION6,
            '7': question.OPTION7,
            '8': question.OPTION8,
            'nan': 'nan'
        }
        job_seeker_answer = option_map.get(selected_option_index, 'nan')

        # Check if answer is correct
        is_correct = job_seeker_answer == question.ANSWERS

        # Save the answer in Cognitive_NVI_Answers_Dataset
        Cognitive_NVI_Answers_Dataset.objects.create(
            COGNITIVE_ASSESSMENT_ID_id=cognitive_assessment_id,
            NVI_IMAGE_QUESTION_ID=question,
            JOB_SEEKER_ANS=job_seeker_answer,
            IS_CORRECT=is_correct
        )

        # Save time taken for the question
        time_taken = int(request.POST.get('time_taken', 60))  # Default 60 if time_taken not present
        cog_nvi_time = request.session.get('cog_nvi_time', 0) + time_taken
        request.session['cog_nvi_time'] = cog_nvi_time

        # Redirect to next question or completion
        if next_question_index is not None:
            return redirect('non_verbal_quiz', question_index=next_question_index)
        else:
            # End of quiz, reset time and go to completion
            # request.session['cog_nvi_time'] = 0
            return redirect('non_verbal_completion')

    options = [
        question.OPTION1.strip(), question.OPTION2.strip(),
        question.OPTION3.strip(), question.OPTION4.strip(),
        question.OPTION5.strip(), question.OPTION6.strip(),
        question.OPTION7.strip(), question.OPTION8.strip()
    ]

    # Filter out options that are "nan"
    options = [option for option in options if option and option.lower() != "nan"]

    current_question_number = question_index + 1
    total_questions = len(selected_questions)
    
    # Calculate progress percentage
    progress_percentage = (current_question_number / total_questions) * 100

    context = {
        'question': question,
        'next_question_index': next_question_index,
        'total_questions': total_questions,
        'current_question_number': current_question_number,
        'options': options,
        'progress_percentage': progress_percentage
    }

    return render(request, 'non_verbal_quiz/non_verbal_quiz.html', context)

def non_verbal_completion(request):
    # Retrieve the `cognitive_assessment_id` from the session
    cognitive_assessment_id = request.session.get('COGNITIVE_ASSESSMENT_ID')

    # Retrieve `VI_COMPLETION_TIME` and `NVI_COMPLETION_TIME` from session
    vi_completion_time = request.session.get('cog_vi_time', 0)
    nvi_completion_time = request.session.get('cog_nvi_time', 0)

    if not cognitive_assessment_id:
        # Redirect to home or show an error if no assessment ID is available
        return redirect('jobseeker_home')

    # If the total time is zero, prevent further processing
    if vi_completion_time == 0 or nvi_completion_time == 0:
        del request.session['selected_technical_questions']
        print("Deleting selected_tech questions")
        # Render a message or simply redirect to prevent duplicate entry
        return render(request, 'non_verbal_quiz/non_verbal_completion.html', {
            'message': "Assessment already completed."
        })

    # Calculate `COGNITIVE_VI_SCORE` as the count of true answers in `Cognitive_VI_Answers_Dataset`
    cognitive_vi_score = Cognitive_VI_Answers_Dataset.objects.filter(
        COGNITIVE_ASSESSMENT_ID=cognitive_assessment_id,
        IS_CORRECT=True
    ).count()

    # Calculate `COGNITIVE_NVI_SCORE` as the count of true answers in `Cognitive_NVI_Answers_Dataset`
    cognitive_nvi_score = Cognitive_NVI_Answers_Dataset.objects.filter(
        COGNITIVE_ASSESSMENT_ID=cognitive_assessment_id,
        IS_CORRECT=True
    ).count()

    # `TOTAL_COGNITIVE_SCORE` is the sum of `COGNITIVE_VI_SCORE` and `COGNITIVE_NVI_SCORE`
    total_cognitive_score = cognitive_vi_score + cognitive_nvi_score

    # `COGNITIVE_SCORE_PERCENTAGE` is `(TOTAL_COGNITIVE_SCORE / 30) * 100`
    cognitive_score_percentage = int((total_cognitive_score / 30) * 100)

    

    # `TOTAL_COGNITIVE_COMPLETION_TIME` is the sum of `VI_COMPLETION_TIME` and `NVI_COMPLETION_TIME`
    total_cognitive_completion_time = vi_completion_time + nvi_completion_time

    # Create `Cognitive_Assessment_Results` entry
    Cognitive_Assessment_Results.objects.create(
        COGNITIVE_ASSESSMENT_ID_id=cognitive_assessment_id,
        COGNITIVE_VI_SCORE=cognitive_vi_score,
        COGNITIVE_NVI_SCORE=cognitive_nvi_score,
        TOTAL_COGNITIVE_SCORE=total_cognitive_score,
        COGNITIVE_SCORE_PERCENTAGE=cognitive_score_percentage,
        VI_COMPLETION_TIME=str(vi_completion_time),  # Convert to string if necessary
        NVI_COMPLETION_TIME=str(nvi_completion_time),  # Convert to string if necessary
        TOTAL_COGNITIVE_COMPLETION_TIME=str(total_cognitive_completion_time)  # Convert to string if necessary
    )

    # Reset time-related session variables to prevent data leakage between assessments
    request.session['cog_vi_time'] = 0
    request.session['cog_nvi_time'] = 0

    # Render the completion template
    return render(request, 'non_verbal_quiz/non_verbal_completion.html')
#* ------------------------------------------------------------------------------------------
#* --------------------------------------[ ENDS ]--------------------------------------------
#* ------------------------------------------------------------------------------------------

#* ------------------------------------------------------------------------------------------
#* -----------------------[ TECHNICAL QUIZ INTEGRATED ]--------------------------------------
#* ------------------------------------------------------------------------------------------
def technical_quiz_start_redirect(request):
    # Ensure this view is only accessed via a POST request
    if request.method == 'POST':
        # Step 1: Remove the old JOB_SEEKER_ASSESSMENT_ID from session if exists
        if 'JOB_SEEKER_ASSESSMENT_ID' in request.session:
            del request.session['JOB_SEEKER_ASSESSMENT_ID']
        
        # Retrieve required values from session
        job_seeker_id = request.session.get('JOB_SEEKER_ID')
        job_post_id = request.session.get('JOB_POST_ID')
        assessment_id = request.session.get('ASSESSMENT_ID')

        # Fetch the `Job_Seeker` instance using `job_seeker_id`
        job_seeker = Job_Seeker.objects.get(JOB_SEEKER_ID=job_seeker_id)

        # Fetch user's first name from `User_Information`
        user_info = User_Information.objects.get(USER_ID=job_seeker.USER_ID)
        first_name = user_info.FIRST_NAME

        # Create a new `Job_Seeker_Assessment` record
        job_seeker_assessment = Job_Seeker_Assessment.objects.create(
            JOB_SEEKER_ID=job_seeker,
            JOB_POST_ID_id=job_post_id,
            ASSESSMENT_ID_id=assessment_id,
            NAME=first_name,
            ASSESSMENT_TYPE="Technical Assessment",
            TOTAL_COMPLETION_TIME_REQUIRED="900"  # Static value as specified
        )
        
        # Save the newly created `JOB_SEEKER_ASSESSMENT_ID` in session
        request.session['JOB_SEEKER_ASSESSMENT_ID'] = job_seeker_assessment.JOB_SEEKER_ASSESSMENT_ID
        
        # Fetch the `TECHNICAL_ASSESSMENT_LEVEL` from the `Assessment` table
        assessment = Assessment.objects.get(ASSESSMENT_ID=assessment_id)
        technical_assessment_level = assessment.TECHNICAL_ASSESSMENT_LEVEL

        # Step 2: Populate the `Technical_Assessment` table
        technical_assessment = Technical_Assessment.objects.create(
            JOB_SEEKER_ASSESSMENT_ID=job_seeker_assessment,
            TECHNICAL_ASSESSMENT_LEVEL=technical_assessment_level,  # Value from the Assessment table
            TECHNICAL_COMPLETION_TIME_REQUIRED="900"  # Static value as specified
        )
        
        # Save the `TECHNICAL_ASSESSMENT_ID` in session for further use
        request.session['TECHNICAL_ASSESSMENT_ID'] = technical_assessment.TECHNICAL_ASSESSMENT_ID
        
        # Step 3: Redirect to the start of the technical quiz
        return redirect('technical_quiz_start')
    
    # Fallback in case of non-POST request
    return redirect('jobseeker_home')


# def technical_quiz_start(request):
#     if 'selected_technical_questions' not in request.session:
#         question_ids = list(Technical_Questions_Dataset.objects.values_list('TECH_ID', flat=True))
#         selected_questions = random.sample(question_ids, 15) if len(question_ids) >= 15 else question_ids
#         request.session['selected_technical_questions'] = selected_questions
#     return redirect('technical_quiz', question_index=0)

def technical_quiz_start(request):
    # Assuming 'job_post_id' is passed in session or request, depending on your setup
    job_post_id = request.session.get('JOB_POST_ID')  # or request.GET.get('job_post_id') if passed as GET parameter

    if not job_post_id:
        print("No job_post_id found in session.")
        return redirect('jobseeker_home')  # Redirect to an error page if job_post_id is missing

    # Fetch the Job Position and Technical Assessment Level from the Job Posting
    try:
        job_post = Job_Posting.objects.get(JOB_POST_ID=job_post_id)
        job_position = job_post.JOB_POSITION.strip()  # Ensure no trailing whitespace
        assessment_level = [level.strip() for level in job_post.TECHNICAL_ASSESSMENT_LEVEL.split(',')]
        print(f"Job Position from Job Posting: {job_position}")
        print(f"Technical Assessment Levels from Job Posting: {assessment_level}")
    except Job_Posting.DoesNotExist:
        print(f"Job Posting with ID {job_post_id} does not exist.")
        return redirect('jobseeker_home')  # Redirect to an error page if job_post_id is invalid

    # If 'selected_technical_questions' not in session, filter and select random questions
    if 'selected_technical_questions' not in request.session:
        print("Entering question selection block.")
        
        # Filter questions by Job Position and Test Level
        filtered_questions = Technical_Questions_Dataset.objects.filter(
            JOB_POSITION=job_position,
            TEST_LEVEL__in=assessment_level  # Corrected to use __in lookup for list filtering
        ).values_list('TECH_ID', flat=True)

        # Debug information for filtered questions
        print(f"Filtered Questions for Job Position '{job_position}' and Assessment Levels '{assessment_level}': {list(filtered_questions)}")

        # Get 15 random questions if available, otherwise select all
        question_ids = list(filtered_questions)
        if question_ids:
            selected_questions = random.sample(question_ids, 15) if len(question_ids) >= 15 else question_ids
            print(f"Selected Question IDs: {selected_questions}")

            # Store selected questions in session
            request.session['selected_technical_questions'] = selected_questions
        else:
            print("No questions found for the specified Job Position and Assessment Levels.")
            return redirect('jobseeker_home')  # Redirect if no questions match the criteria

    return redirect('technical_quiz', question_index=0)


def technical_quiz(request, question_index=0):
    selected_questions = request.session.get('selected_technical_questions', [])
    
    if not selected_questions:
        return redirect('technical_quiz_start')

    question_id = selected_questions[question_index]
    question = get_object_or_404(Technical_Questions_Dataset, TECH_ID=question_id)
    next_question_index = question_index + 1 if question_index < len(selected_questions) - 1 else None

    technical_assessment_id = request.session.get('TECHNICAL_ASSESSMENT_ID')
    
    if request.method == 'POST':
        selected_option = request.POST.get('option', 'nan')

        is_correct = selected_option == question.ANSWER

        Technical_Answers_Dataset.objects.create(
            TECH_ID=question,
            TECHNICAL_ASSESSMENT_ID_id=technical_assessment_id,
            JOB_SEEKER_ANS=selected_option,
            IS_CORRECT=is_correct
        )
        
        # Save the time taken
        time_taken = request.POST.get('time_taken', 60)
        tech_time = request.session.get('tech_time', 0) + int(time_taken)
        request.session['tech_time'] = tech_time

        # Redirect to the next question or completion
        if next_question_index is not None:
            return redirect('technical_quiz', question_index=next_question_index)
        else:
            return redirect('technical_quiz_completion')

    options = [
        question.A.strip(), question.B.strip(),
        question.C.strip(), question.D.strip()
    ]

    current_question_number = question_index + 1
    total_questions = len(selected_questions)
    
    # Calculate progress percentage
    progress_percentage = (current_question_number / total_questions) * 100

    context = {
        'question': question,
        'next_question_index': next_question_index,
        'total_questions': total_questions,
        'current_question_number': current_question_number,
        'options': options,
        'progress_percentage': progress_percentage
    }

    return render(request, 'technical_quiz/technical_quiz.html', context)

def technical_quiz_completion(request):
    technical_assessment_id = request.session.get('TECHNICAL_ASSESSMENT_ID')
    
    # Get the total technical completion time from the session
    total_technical_completion_time = request.session.get('tech_time')
    
    # If the total time is zero, prevent further processing
    if total_technical_completion_time == 0:
        # Render a message or simply redirect to prevent duplicate entry
        return render(request, 'technical_quiz/technical_completion.html', {
            'message': "Assessment already completed."
        })

    # Calculate the total correct answers (Total Tech Score)
    total_correct_answers = Technical_Answers_Dataset.objects.filter(
        TECHNICAL_ASSESSMENT_ID=technical_assessment_id,
        IS_CORRECT=True
    ).count()

    # Calculate the tech score percentage
    tech_score_percentage = (total_correct_answers / 15) * 100

    

    # Populate the Technical_Assessment_Result table
    Technical_Assessment_Result.objects.create(
        TECHNICAL_ASSESSMENT_ID_id=technical_assessment_id,
        TOTAL_TECH_SCORE=total_correct_answers,
        TECH_SCORE_PERCENTAGE=tech_score_percentage,
        TOTAL_TECHNICAL_COMPLETION_TIME=total_technical_completion_time
    )

    request.session['tech_time'] = 0


    # List of session keys related to assessments to be cleared
    # keys_to_clear = [
    #     'JOB_POST_ID',
    #     'JOB_SEEKER_ID',
    #     'ASSESSMENT_ID',
    #     'JOB_SEEKER_ASSESSMENT_ID',
    #     'PERSONALITY_ASSESSMENT_ID',
    #     'DISC_ASSESSMENT_ID',
    #     'total_time',
    #     'BIGFIVE_ASSESSMENT_ID',
    #     'COGNITIVE_ASSESSMENT_ID',
    #     'time_taken',
    #     'cog_vi_time',
    #     'cog_nvi_time',
    #     'TECHNICAL_ASSESSMENT_ID',
    #     'verbal_selected_questions',
    #     'selected_questions',
    #     'selected_technical_questions',
    #     'tech_time',
    # ]

    # Delete each key from the session if it exists
    # for key in keys_to_clear:
    #     if key in request.session:
    #         del request.session[key]

    # Render the completion template or redirect as necessary
    return render(request, 'technical_quiz/technical_completion.html')
    # return redirect('process_assessment_and_generate_summary')
#* ------------------------------------------------------------------------------------------
#* -------------------------------[ ENDS ]---------------------------------------------------
#* ------------------------------------------------------------------------------------------

# # ----------------------------[ PHASE COMPLETETIONS Unchanged ]-----------------------------------------
def phase_one_completed(request):
    # Assuming job_seeker_id is stored in session when the user logs in
    job_seeker_id = request.session.get('job_seeker_id')
    if not job_seeker_id:
        return redirect('jobseeker_login')  # Redirect to login if job_seeker_id is not in session

    # Fetch assessment_id and job_post_id from the session
    assessment_id = request.session.get('assessment_id')
    job_post_id = request.session.get('job_post_id')
    if not assessment_id or not job_post_id:
        return redirect('jobseeker_home')  # Redirect to home if IDs are not found

    # Fetch the job seeker, job post, and assessment objects
    job_seeker = Job_Seeker.objects.get(JOB_SEEKER_ID=job_seeker_id)
    job_post = Job_Posting.objects.get(JOB_POST_ID=job_post_id)
    assessment = Assessment.objects.get(ASSESSMENT_ID=assessment_id)

    # Create the Job_Seeker_Assessment record
    job_seeker_assessment = Job_Seeker_Assessment.objects.create(
        JOB_SEEKER_ID=job_seeker,
        JOB_POST_ID=job_post,
        ASSESSMENT_ID=assessment,
        ASSESSMENT_TYPE="Cognitive_nvi, Technical",
    )

    # Store job_seeker_assessment_id in the session
    request.session['job_seeker_assessment_id'] = str(job_seeker_assessment.JOB_SEEKER_ASSESSMENT_ID)

    # Create the Cognitive_Assessment record using the Job_Seeker_Assessment record
    cognitive_assessment = Cognitive_Assessment.objects.create(
        JOB_SEEKER_ASSESSMENT_ID=job_seeker_assessment,
        COGNITIVE_ASSESSMENT_TYPE="Cognitive_nvi"
    )

    # Store cognitive_assessment_id in the session
    request.session['cognitive_assessment_id'] = str(cognitive_assessment.COGNITIVE_ASSESSMENT_ID)

    return render(request, './test_complete/phase_one_completed.html')

def phase_two_completed(request):
    # Fetch job_seeker_assessment_id from the session
    job_seeker_assessment_id = request.session.get('job_seeker_assessment_id')
    if not job_seeker_assessment_id:
        return redirect('jobseeker_home')  # Redirect to home if job_seeker_assessment_id is not found

    # Fetch the Job_Seeker_Assessment object
    job_seeker_assessment = Job_Seeker_Assessment.objects.get(JOB_SEEKER_ASSESSMENT_ID=job_seeker_assessment_id)

    # Calculate the score
    cognitive_assessment_id = request.session.get('cognitive_assessment_id')
    if not cognitive_assessment_id:
        return redirect('jobseeker_home')  # Redirect to home if cognitive_assessment_id is not found

    score = Cognitive_NVI_Answers_Dataset.objects.filter(
        COGNITIVE_ASSESSMENT_ID=cognitive_assessment_id,
        IS_CORRECT=True
    ).count()

    total_questions = 30  # Total number of questions
    score_display = f"{score} / {total_questions}"

    # # Create the Technical_Assessment record using the Job_Seeker_Assessment record
    # Technical_Assessment.objects.create(
    #     JOB_SEEKER_ASSESSMENT_ID=job_seeker_assessment,
    #     TECHNICAL_ASSESSMENT_LEVEL="Technical"
    # )

    # Create the Technical_Assessment record using the Job_Seeker_Assessment record
    technical_assessment = Technical_Assessment.objects.create(
        JOB_SEEKER_ASSESSMENT_ID=job_seeker_assessment,
        TECHNICAL_ASSESSMENT_LEVEL="Technical"
    )

    # Store technical_assessment_id in the session
    request.session['technical_assessment_id'] = str(technical_assessment.TECHNICAL_ASSESSMENT_ID)


    return render(request, './test_complete/phase_two_completed.html', {'score_display': score_display})

def phase_three_completed(request):
    # Fetch technical_assessment_id from the session
    technical_assessment_id = request.session.get('technical_assessment_id')
    if not technical_assessment_id:
        return redirect('jobseeker_home')  # Redirect to home if technical_assessment_id is not found

    # Calculate the score
    score = Technical_Answers_Dataset.objects.filter(
        TECHNICAL_ASSESSMENT_ID=technical_assessment_id,
        IS_CORRECT=True
    ).count()

    total_questions = 30  # Total number of questions
    score_display = f"{score} / {total_questions}"

    return render(request, './test_complete/phase_three_completed.html', {'score_display': score_display})

# # ------------------------------------[ ENDS ]-----------------------------------------------

# ---------------------------------[ for generating the evaluation summary using ChatGPT ]-----------------------------------------
def process_assessment_and_generate_summary(request):
    # Initialize the gpt variable first
    chatgpt = ChatGPTIntegration()

    # Getting all ids available in the session
    user_id = request.session.get('user_id')  # The user ID from session
    job_seeker_id = request.session.get('JOB_SEEKER_ID')
    assessment_id = request.session.get('ASSESSMENT_ID')
    personality_assessment_id = request.session.get('PERSONALITY_ASSESSMENT_ID')
    cognitive_assessment_id = request.session.get('COGNITIVE_ASSESSMENT_ID')
    technical_assessment_id = request.session.get('TECHNICAL_ASSESSMENT_ID')

    # Step 1: Retrieve the instances from each model using the IDs from the session
    try:
        user_info = User_Information.objects.get(USER_ID=user_id)  # Retrieve User_Information instance
        job_seeker = Job_Seeker.objects.get(JOB_SEEKER_ID=job_seeker_id)  # Retrieve Job_Seeker instance
        assessment = Assessment.objects.get(ASSESSMENT_ID=assessment_id)  # Retrieve Assessment instance
        personality_assessment_report = Personality_Assessment_Report.objects.get(PERSONALITY_ASSESSMENT_ID=personality_assessment_id)  # Retrieve Personality Assessment Report instance
        cognitive_assessment = Cognitive_Assessment_Results.objects.get(COGNITIVE_ASSESSMENT_ID=cognitive_assessment_id)  # Retrieve Cognitive Assessment Results instance
        technical_assessment = Technical_Assessment_Result.objects.get(TECHNICAL_ASSESSMENT_ID=technical_assessment_id)  # Retrieve Technical Assessment Results instance
    except (User_Information.DoesNotExist, Job_Seeker.DoesNotExist, Assessment.DoesNotExist, Personality_Assessment_Report.DoesNotExist, Cognitive_Assessment_Results.DoesNotExist, Technical_Assessment_Result.DoesNotExist) as e:
        return HttpResponse(f"Error: {str(e)}", status=404)

    # Continue with the rest of your logic...
    cognitive_weightage = int(assessment.COGNITIVE_WEIGHTAGE)
    technical_weightage = int(assessment.TECHNICAL_WEIGHTAGE)
    job_post_id = assessment.JOB_POST_ID

    # Step 2: Retrieve the Job_Posting Table
    job_post = Job_Posting.objects.get(JOB_POST_ID=job_post_id)

    # Initialize an empty personality_report_fields in case conditions are not met
    personality_report_fields = {}

    personality_report_fields = {
            "DISC_CATEGORY": personality_assessment_report.DISC_CATEGORY,
            "DISC_PERSONALITY_TRAIT": personality_assessment_report.DISC_PERSONALITY_TRAIT,
            "DISC_COGNITIVE_ABILITY": personality_assessment_report.DISC_COGNITIVE_ABILITY,
            "DISC_EMOTIONAL_REGULATION": personality_assessment_report.DISC_EMOTIONAL_REGULATION,
            "DISC_TENDENCIES": personality_assessment_report.DISC_TENDENCIES,
            "DISC_WEAKNESSES": personality_assessment_report.DISC_WEAKNESSES,
            "DISC_BEHAVIOUR": personality_assessment_report.DISC_BEHAVIOUR,
            "DISC_MOTIVATED_BY": personality_assessment_report.DISC_MOTIVATED_BY,
            "BIGFIVE_OPENNESS_CATEGORY": personality_assessment_report.BIGFIVE_OPENNESS_CATEGORY,
            "BIGFIVE_OPENNESS_PERSONALITY": personality_assessment_report.BIGFIVE_OPENNESS_PERSONALITY,
            "BIGFIVE_OPENNESS_DESCRIPTION": personality_assessment_report.BIGFIVE_OPENNESS_DESCRIPTION,
            "BIGFIVE_OPENNESS_WORKPLACE_BEHAVIOUR": personality_assessment_report.BIGFIVE_OPENNESS_WORKPLACE_BEHAVIOUR,
            "BIGFIVE_CONCIENTIOUSNESS_CATEGORY": personality_assessment_report.BIGFIVE_CONCIENTIOUSNESS_CATEGORY,
            "BIGFIVE_CONCIENTIOUSNESS_PERSONALITY": personality_assessment_report.BIGFIVE_CONCIENTIOUSNESS_PERSONALITY,
            "BIGFIVE_CONCIENTIOUSNESS_DESCRIPTION": personality_assessment_report.BIGFIVE_CONCIENTIOUSNESS_DESCRIPTION,
            "BIGFIVE_CONCIENTIOUSNESS_WORKPLACE_BEHAVIOUR": personality_assessment_report.BIGFIVE_CONCIENTIOUSNESS_WORKPLACE_BEHAVIOUR,
            "BIGFIVE_EXTRAVERSION_CATEGORY": personality_assessment_report.BIGFIVE_EXTRAVERSION_CATEGORY,
            "BIGFIVE_EXTRAVERSION_PERSONALITY": personality_assessment_report.BIGFIVE_EXTRAVERSION_PERSONALITY,
            "BIGFIVE_EXTRAVERSION_DESCRIPTION": personality_assessment_report.BIGFIVE_EXTRAVERSION_DESCRIPTION,
            "BIGFIVE_EXTRAVERSION_WORKPLACE_BEHAVIOUR": personality_assessment_report.BIGFIVE_EXTRAVERSION_WORKPLACE_BEHAVIOUR,
            "BIGFIVE_AGREEABLENESS_CATEGORY": personality_assessment_report.BIGFIVE_AGREEABLENESS_CATEGORY,
            "BIGFIVE_AGREEABLENESS_PERSONALITY": personality_assessment_report.BIGFIVE_AGREEABLENESS_PERSONALITY,
            "BIGFIVE_AGREEABLENESS_DESCRIPTION": personality_assessment_report.BIGFIVE_AGREEABLENESS_DESCRIPTION,
            "BIGFIVE_AGREEABLENESS_WORKPLACE_BEHAVIOUR": personality_assessment_report.BIGFIVE_AGREEABLENESS_WORKPLACE_BEHAVIOUR,
            "BIGFIVE_NEUROTICISM_CATEGORY": personality_assessment_report.BIGFIVE_NEUROTICISM_CATEGORY,
            "BIGFIVE_NEUROTICISM_PERSONALITY": personality_assessment_report.BIGFIVE_NEUROTICISM_PERSONALITY,
            "BIGFIVE_NEUROTICISM_DESCRIPTION": personality_assessment_report.BIGFIVE_NEUROTICISM_DESCRIPTION,
            "BIGFIVE_NEUROTICISM_WORKPLACE_BEHAVIOUR": personality_assessment_report.BIGFIVE_NEUROTICISM_WORKPLACE_BEHAVIOUR
        }

    if cognitive_assessment.COGNITIVE_SCORE_PERCENTAGE < cognitive_weightage:
        candidate_status = "Not Recommended"
    elif technical_assessment.TECH_SCORE_PERCENTAGE < technical_weightage:
        candidate_status = "Not Recommended"
    else:
        try:
            candidate_status = chatgpt.generate_candidate_status(personality_report_fields, job_post.JOB_POSITION)
            print(f'CHECKING THE PERSONALITY REPORT-----------{personality_report_fields}-------------')
        except Exception as e:
            print(f"Error with OpenAI API call for candidate status: {str(e)}")
            candidate_status = "unknown"


    try:
        profile_synopsis = chatgpt.generate_profile_synopsis(personality_report_fields)
        optimal_job_matches = chatgpt.generate_optimal_job_matches(personality_report_fields)
    except Exception as e:
        profile_synopsis = "unknown"
        optimal_job_matches = "unknown"

    # Step 7: Save to Evaluation_Summary table by assigning only the IDs (foreign keys)
    evaluation_summary = Evaluation_Summary.objects.create(
        USER_ID=user_info,  # Assign the instance of User_Information, not just the ID
        JOB_SEEKER_ID=job_seeker,  # Assign the instance of Job_Seeker
        JOB_POST_ID=job_post,  # Assign the instance of Job_Posting
        ASSESSMENT_ID=assessment,  # Assign the instance of Assessment
        PERSONALITY_ASSESSMENT_REPORT_ID=personality_assessment_report,  # Assign the instance of Personality Assessment Report
        COGNITIVE_ASSESSMENT_RESULT_ID=cognitive_assessment,  # Assign the instance of Cognitive Assessment Results
        TECHNICAL_ASSESSMENT_RESULT_ID=technical_assessment,  # Assign the instance of Technical Assessment Result
        CANDIDATE_STATUS=candidate_status,
        PROFILE_SYNOPSIS=profile_synopsis,
        OPTIMAL_JOB_MATCHES=optimal_job_matches
    )

    evaluation_summary.save()

    request.session['EVALUATION_SUMMARY_ID'] = evaluation_summary.EVALUATION_SUMMARY_ID

    # return render(request, 'report/report.html')
    return redirect('job_seeker_report')

def job_seeker_report(request):
    evaluation_summary_id = request.session.get('EVALUATION_SUMMARY_ID')
    print(f'------------The Id got on this page is this: {evaluation_summary_id}-------------')
    try:
        # Retrieve the Evaluation_Summary instance using the ID
        evaluation_summary = Evaluation_Summary.objects.get(EVALUATION_SUMMARY_ID=evaluation_summary_id)
        
        # Extract related information using the foreign keys
        user_info = evaluation_summary.USER_ID
        job_post = evaluation_summary.JOB_POST_ID
        personality_report = evaluation_summary.PERSONALITY_ASSESSMENT_REPORT_ID
        cognitive_assessment = evaluation_summary.COGNITIVE_ASSESSMENT_RESULT_ID
        technical_assessment = evaluation_summary.TECHNICAL_ASSESSMENT_RESULT_ID


        # All Data that are in commas will be comma seperated here
        # -- From Job Post ----
        personality_traits_list = [trait.strip() for trait in job_post.PERSONALITY_TRAITS.split(",")]
        technical_assessment_level_list = [level.strip() for level in job_post.TECHNICAL_ASSESSMENT_LEVEL.split(",")]
        
        # -- From PERSONALITY REPORT ----
        disc_personality_trait_list = [trait.strip() for trait in personality_report.DISC_PERSONALITY_TRAIT.split(",")]
        bigf_openness_personality_list = [personality.strip() for personality in personality_report.BIGFIVE_OPENNESS_PERSONALITY.split(",")]
        bigf_concientiousness_personality_list = [personality.strip() for personality in personality_report.BIGFIVE_CONCIENTIOUSNESS_PERSONALITY.split(",")]
        bigf_extraversion_personality_list = [personality.strip() for personality in personality_report.BIGFIVE_EXTRAVERSION_PERSONALITY.split(",")]
        bigf_agreeableness_personality_list = [personality.strip() for personality in personality_report.BIGFIVE_AGREEABLENESS_PERSONALITY.split(",")]
        bigf_neuroticism_personality_list = [personality.strip() for personality in personality_report.BIGFIVE_NEUROTICISM_PERSONALITY.split(",")]
        disc_cognitive_abilities_list = [ability.strip() for ability in personality_report.DISC_COGNITIVE_ABILITY.split(",")]
        disc_tendencies_list = [tendency.strip() for tendency in personality_report.DISC_TENDENCIES.split(",")]
        disc_weaknesses_list = [weakness.strip() for weakness in personality_report.DISC_WEAKNESSES.split(",")]
        disc_behaviour_list = [behaviour.strip() for behaviour in personality_report.DISC_BEHAVIOUR.split(",")]
        disc_motivated_list = [motivate.strip() for motivate in personality_report.DISC_MOTIVATED_BY.split(",")]
        disc_emotional_list = [emotion.strip() for emotion in personality_report.DISC_EMOTIONAL_REGULATION.split(",")]
        

        #  -- From Cognitive Assessment
        if int(cognitive_assessment.COGNITIVE_SCORE_PERCENTAGE) >= int(job_post.COGNITIVE_WEIGHTAGE):
            cognitive_result = "Passed"
        else:
            cognitive_result = "Failed"

        if int(technical_assessment.TECH_SCORE_PERCENTAGE) >= int(job_post.TECHNICAL_WEIGHTAGE):
            technical_result = "Passed"
        else:
            technical_result = "Failed"

        # -- From Evaluation Summary
        # optimal_job_matches_list = [match.strip() for match in evaluation_summary.OPTIMAL_JOB_MATCHES.split(". ")]
        optimal_job_matches_list = [match.strip() for match in re.split(r'\d+\.\s+', evaluation_summary.OPTIMAL_JOB_MATCHES) if match.strip()]
        if evaluation_summary.CANDIDATE_STATUS == "Not Recommended":
            candidate_status = "Not Recommended"
        else:
            candidate_status = "Recommended"

        # Prepare the context to send to the template
        context = {
            'evaluation_summary': evaluation_summary,
            'user_info': user_info,
            'job_post': job_post,
            'personality_traits_list': personality_traits_list,
            'tech_assessment_level_list': technical_assessment_level_list,
            'disc_personality_trait_list': disc_personality_trait_list,
            'bigf_openness_personality_list': bigf_openness_personality_list,
            'bigf_concientiousness_personality_list': bigf_concientiousness_personality_list,
            'bigf_extraversion_personality_list': bigf_extraversion_personality_list,
            'bigf_agreeableness_personality_list': bigf_agreeableness_personality_list,
            'bigf_neuroticism_personality_list': bigf_neuroticism_personality_list,
            'disc_cognitive_abilities_list': disc_cognitive_abilities_list,
            'disc_tendencies_list': disc_tendencies_list,
            'disc_weaknesses_list': disc_weaknesses_list,
            'disc_behaviour_list': disc_behaviour_list,
            'disc_motivated_list': disc_motivated_list,
            'disc_emotional_list': disc_emotional_list,
            'personality_report': personality_report,
            'cognitive_assessment': cognitive_assessment,
            'cognitive_result': cognitive_result,
            'technical_result': technical_result,
            'technical_assessment': technical_assessment,
            'candidate_status': candidate_status,
            'optimal_job_matches_list': optimal_job_matches_list,
        }
    except Evaluation_Summary.DoesNotExist:
        # If no evaluation summary found, show an error or redirect
        return HttpResponse("Evaluation Summary not found", status=404)
    
    return render(request, 'report/job_seeker/report.html', context)

def go_home_jobseeker(request):
    # List of session keys related to assessments to be cleared
    keys_to_clear = [
        'JOB_POST_ID',
        'JOB_SEEKER_ID',
        'ASSESSMENT_ID',
        'JOB_SEEKER_ASSESSMENT_ID',
        'PERSONALITY_ASSESSMENT_ID',
        'DISC_ASSESSMENT_ID',
        'total_time',
        'BIGFIVE_ASSESSMENT_ID',
        'COGNITIVE_ASSESSMENT_ID',
        'time_taken',
        'cog_vi_time',
        'cog_nvi_time',
        'TECHNICAL_ASSESSMENT_ID',
        'verbal_selected_questions',
        'selected_questions',
        'selected_technical_questions',
        'tech_time',
        'EVALUATION_SUMMARY_ID'
    ]

    # Delete each key from the session if it exists
    for key in keys_to_clear:
        if key in request.session:
            del request.session[key]

    return redirect('jobseeker_home')
# ---------------------------------[ END ]-----------------------------------------
