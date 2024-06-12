from django.shortcuts import render , get_object_or_404 , redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse
from django.contrib import messages
from .models import DISC_Questions_Dataset, Cognitive_NVI_Questions_Dataset, Technical_Questions_Dataset , Job_Position_Criteria ,User_Information, Job_Seeker, Job_Seeker_Education, Job_Seeker_Work_Experience , Recruiter, Job_Posting , Assessment , Job_Seeker_Assessment, Cognitive_Assessment , Cognitive_NVI_Answers_Dataset, Technical_Assessment, Technical_Answers_Dataset
from .forms import UserInformationForm, JobSeekerForm, JobSeekerEducationForm, JobSeekerWorkExperienceForm , RecruiterForm , JobPostingForm
import random
from datetime import datetime
import json

# ---------------------------------[ START SCREEN ]-----------------------------------------
def start_screen(request):
    return render(request, './start-screen/start_screen.html')
# -------------------------------------[ ENDS ]---------------------------------------------


# ---------------------------------[ LOGIN/LOGOUT ]------------------------------------------
def jobseeker_login(request):
    if request.method == 'POST':
        email = request.POST['email']
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

    return render(request, './login/jobseeker_login.html')

def recruiter_login(request):
    if request.method == 'POST':
        email = request.POST['email']
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

    return render(request, './login/recruiter_login.html')


def jobseeker_logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('jobseeker_login')  # Redirect to the login page or home page after logout

def recruiter_logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('recruiter_login')  # Redirect to the login page or home page after logout
# --------------------------------------[ ENDS ]---------------------------------------------

# ---------------------------------[ JOB SEEKER HOME ]---------------------------------------
def jobseeker_home(request):
    user_id = request.session.get('user_id')
    if user_id:
        user_info = User_Information.objects.get(USER_ID=user_id)
        job_postings = Job_Posting.objects.all()  # Get all job postings
        formatted_job_postings = [format_job_posting_data(job) for job in job_postings]

        return render(request, 'home/jobseeker_home.html', {
            'user_info': user_info,
            'job_postings': formatted_job_postings
        })
    else:
        return redirect('jobseeker_login')  # Redirect to login if not logged in
# --------------------------------------[ ENDS ]---------------------------------------------


# ---------------------------------[ RECRUITER HOME ]----------------------------------------
def recruiter_home(request):
    user_id = request.session.get('user_id')
    if user_id:
        user_info = User_Information.objects.get(USER_ID=user_id)
        recruiter = Recruiter.objects.get(USER_ID=user_info)
        job_postings = Job_Posting.objects.filter(RECRUITER_ID=recruiter)
        formatted_job_postings = [format_job_posting_data(job) for job in job_postings]

        return render(request, 'home/recruiter_home.html', {
            'user_info': user_info,
            'job_postings': formatted_job_postings
        })
    else:
        return redirect('recruiter_login')  # Redirect to login if not logged in
# --------------------------------------[ ENDS ]---------------------------------------------

# ---------------------------------[ JOB POSTINGs RELATED ]----------------------------------
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
        'required_qualifications': job_posting.REQUIRED_QUALIFICATIONS.split(', '),
        'required_skills': job_posting.REQUIRED_SKILLS.split(', '),
        'experience_requirements': job_posting.EXPERIENCE_REQUIREMENTS.split(', '),
        'personality_traits': job_posting.PERSONALITY_TRAITS.split(', '),
        'required_assessments': job_posting.REQUIRED_ASSESSMENTS.split(', '),
        'test_criteria': job_posting.TEST_CRITERIA.split(', '),
    }
    return formatted_data

def post_job(request):
    if request.method == 'POST':
        # Debug: Print request.POST
        print(json.dumps(request.POST, indent=4))

        try:
            user_id = request.session.get('user_id')
            recruiter = Recruiter.objects.get(USER_ID__USER_ID=user_id)  # Get recruiter by user ID

            job_title = request.POST['jobTitle']
            company_name = request.POST['companyName']
            city = request.POST['city']
            country = request.POST['country']
            job_type = request.POST['jobType']
            job_position = request.POST['jobPosition']
            job_description = request.POST['jobDescription']
            contact_information = request.POST['contactInformation']
            
            required_qualifications = ', '.join(request.POST.getlist('requiredQualifications[]'))
            required_skills = ', '.join(request.POST.getlist('requiredSkills[]'))
            experience_requirements = ', '.join(request.POST.getlist('experienceRequirements[]'))
            personality_traits = ', '.join(request.POST.getlist('personalityTraits'))
            
            # Handling assessments
            assessments = []
            if request.POST.get('DISC'):
                assessments.append('DISC')
            if request.POST.get('BigFive'):
                assessments.append('Big Five')
            if request.POST.get('nonVerbal'):
                assessments.append('Non-Verbal')
            if request.POST.get('verbal'):
                assessments.append('Verbal')
            if request.POST.get('beginner'):
                assessments.append('Beginner')
            if request.POST.get('intermediate'):
                assessments.append('Intermediate')
            if request.POST.get('professional'):
                assessments.append('Professional')
            required_assessments = ', '.join(assessments)
            
            # JPC_ID is optional
            jpc_id = ''

            # Static Test Criteria defined
            test_criteria = "of the assessment weight is allocated to the Cognitive Assessment (Non-Verbal only). , of the assessment weight is allocated to the Technical Assessment (from the two chosen difficulty levels)"

            # Save to database
            job_posting = Job_Posting(
                TITLE=job_title,
                DESCRIPTION=job_description,
                RECRUITER_ID=recruiter,
                JPC_ID=jpc_id,
                CITY=city,
                COUNTRY=country,
                JOB_TYPE=job_type,
                JOB_POSITION=job_position,
                PERSONALITY_TRAITS=personality_traits,
                REQUIRED_SKILLS=required_skills,
                REQUIRED_QUALIFICATIONS=required_qualifications,
                EXPERIENCE_REQUIREMENTS=experience_requirements,
                REQUIRED_ASSESSMENTS=required_assessments,
                TEST_CRITERIA=test_criteria
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
    return render(request, './post_job/post_job.html', {'job_positions': job_positions})

def get_personality_traits(request):
    job_position = request.GET.get('job_position')
    print("Received job position:", job_position)
    for criteria in Job_Position_Criteria.objects.all():
        print('Checking the data of Job Positions: ',criteria.JOB_POSITION)
    if job_position:
        job_position = job_position + " "
        criteria = Job_Position_Criteria.objects.filter(JOB_POSITION=job_position)
        print("Matching criteria:", criteria)
        print("Matching criteria count:", criteria.count())
        if criteria.exists():
            personality_traits = set()
            for criterion in criteria:
                if criterion.PERSONALITY_TRAITS and criterion.PERSONALITY_TRAITS.lower() != 'nan':
                    personality_traits.add(criterion.PERSONALITY_TRAITS)
                if criterion.COGNITIVE_SKILLS and criterion.COGNITIVE_SKILLS.lower() != 'nan':
                    personality_traits.add(criterion.COGNITIVE_SKILLS)
                if criterion.EMOTIONAL_INTELLIGENCE and criterion.EMOTIONAL_INTELLIGENCE.lower() != 'nan':
                    personality_traits.add(criterion.EMOTIONAL_INTELLIGENCE)
            print("Extracted personality traits:", personality_traits)
            return JsonResponse({'personality_traits': list(personality_traits)})
        else:
            print("No matching criteria found")
    else:
        print("No job position provided")
    return JsonResponse({'personality_traits': []})

def apply_for_job(request, job_post_id):
    if request.method == 'POST':
        # Hardcoded assessment categories
        assessment_categories = ["Cognitive_nvi", "Technical"]
        assessment_category_str = ', '.join(assessment_categories)

        # Create a single assessment record with combined categories
        assessment = Assessment.objects.create(
            ASSESSMENT_CATEGORY=assessment_category_str
        )

        # Store assessment_id and job_post_id in the session
        request.session['assessment_id'] = str(assessment.ASSESSMENT_ID)
        request.session['job_post_id'] = job_post_id

        # Redirect to the quiz start screen
        return redirect('quiz_start_screen')
    else:
        # If not a POST request, redirect back to jobseeker home
        return redirect('jobseeker_home')

# ----------------------------[ CREATE ACCOUNT JS ]------------------------------------------
def job_seeker_create_account_step1(request):
    if request.method == 'POST':
        form = UserInformationForm(request.POST)
        if form.is_valid():
            user = form.save()
            request.session['user_id'] = str(user.USER_ID)
            request.session['user_data'] = form.cleaned_data
            return redirect('job_seeker_create_account_step2')
    else:
        form = UserInformationForm()

    return render(request, 'create_account/job_seeker_create_account_step1.html', {'form': form})

def job_seeker_create_account_step2(request):
    if request.method == 'POST':
        form = JobSeekerEducationForm(request.POST)
        if form.is_valid():
            education_data = form.cleaned_data
            education_data['START_DATE'] = education_data['START_DATE'].isoformat()
            education_data['END_DATE'] = education_data['END_DATE'].isoformat()
            request.session['education_data'] = education_data
            return redirect('job_seeker_create_account_step3')
    else:
        form = JobSeekerEducationForm()

    return render(request, 'create_account/job_seeker_create_account_step2.html', {'form': form})

def job_seeker_create_account_step3(request):
    if request.method == 'POST':
        form = JobSeekerWorkExperienceForm(request.POST)
        if form.is_valid():
            work_experience_data = form.cleaned_data
            work_experience_data['START_DATE'] = work_experience_data['START_DATE'].isoformat()
            work_experience_data['END_DATE'] = work_experience_data['END_DATE'].isoformat()
            request.session['work_experience_data'] = work_experience_data
            return redirect('job_seeker_create_account_step4')
    else:
        form = JobSeekerWorkExperienceForm()

    return render(request, 'create_account/job_seeker_create_account_step3.html', {'form': form})

def job_seeker_create_account_step4(request):
    if request.method == 'POST':
        form = JobSeekerForm(request.POST, request.FILES)
        if form.is_valid():
            user_id = request.session.get('user_id')
            education_data = request.session.get('education_data')
            work_experience_data = request.session.get('work_experience_data')

            # Convert date strings back to date objects
            education_data['START_DATE'] = datetime.fromisoformat(education_data['START_DATE'])
            education_data['END_DATE'] = datetime.fromisoformat(education_data['END_DATE'])
            work_experience_data['START_DATE'] = datetime.fromisoformat(work_experience_data['START_DATE'])
            work_experience_data['END_DATE'] = datetime.fromisoformat(work_experience_data['END_DATE'])

            education_form = JobSeekerEducationForm(education_data)
            work_experience_form = JobSeekerWorkExperienceForm(work_experience_data)
            job_seeker_form = JobSeekerForm(request.POST, request.FILES)

            if education_form.is_valid() and work_experience_form.is_valid() and job_seeker_form.is_valid():
                user = User_Information.objects.get(USER_ID=user_id)

                job_seeker = job_seeker_form.save(commit=False)
                job_seeker.USER_ID = user
                job_seeker.save()

                education = education_form.save(commit=False)
                education.JOB_SEEKER_ID = job_seeker
                education.save()

                work_experience = work_experience_form.save(commit=False)
                work_experience.JOB_SEEKER_ID = job_seeker
                work_experience.save()

                return redirect('success_page')  # Redirecting to the success page
    else:
        form = JobSeekerForm()

    return render(request, 'create_account/job_seeker_create_account_step4.html', {'form': form})

def success_page(request):
    return render(request, 'create_account/success.html')
# ------------------------------------[ ENDS ]-----------------------------------------------

# ----------------------------[ CREATE ACCOUNT R ]--------------------------------------------
def recruiter_create_account_step1(request):
    if request.method == 'POST':
        form = UserInformationForm(request.POST)
        if form.is_valid():
            user = form.save()
            request.session['user_id'] = str(user.USER_ID)
            request.session['user_data'] = form.cleaned_data
            return redirect('recruiter_create_account_step2')
    else:
        form = UserInformationForm()

    return render(request, 'create_account/recruiter_create_account_step1.html', {'form': form})

def recruiter_create_account_step2(request):
    if request.method == 'POST':
        form = RecruiterForm(request.POST)
        if form.is_valid():
            user_id = request.session.get('user_id')

            recruiter = form.save(commit=False)
            recruiter.USER_ID = User_Information.objects.get(USER_ID=user_id)
            recruiter.save()

            return redirect('recruiter_success_page')  # Redirecting to the success page
    else:
        form = RecruiterForm()

    return render(request, 'create_account/recruiter_create_account_step2.html', {'form': form})

def recruiter_success_page(request):
    return render(request, 'create_account/recruiter_success.html')
# ------------------------------------[ ENDS ]-----------------------------------------------

# ----------------------------[ QUIZ START ]-------------------------------------------------
def quiz_start_screen(request):
    return render(request, './quiz/quiz_start_screen.html')
# ----------------------------[ DISC QUIZ ]--------------------------------------------------
def disc_quiz_start(request):
    # Redirect to the first question
    first_question = DISC_Questions_Dataset.objects.first()
    if first_question:
        first_question_id = first_question.DISC_PROFILE_ID
        return redirect('disc_quiz', question_id=first_question_id)
    else:
        # Handle the case where there are no questions in the dataset
        return render(request, 'disc_quiz/no_questions.html')

def disc_quiz(request, question_id):
    # Get the question based on the current question ID
    question = get_object_or_404(DISC_Questions_Dataset, DISC_PROFILE_ID=question_id)
    next_question_id = None
    try:
        next_question_id = DISC_Questions_Dataset.objects.filter(DISC_PROFILE_ID__gt=question_id).order_by('DISC_PROFILE_ID').first().DISC_PROFILE_ID
    except AttributeError:
        next_question_id = None

    context = {
        'question': question,
        'next_question_id': next_question_id,
        'total_questions': DISC_Questions_Dataset.objects.count()
    }
    return render(request, 'disc_quiz/disc_quiz.html', context)

def disc_quiz_start_redirect(request):
    return redirect('disc_quiz_start')
# ------------------------------[ ENDS ]----------------------------------------------------


# ----------------------------[ NON VERBAL QUIZ ]--------------------------------------------
def non_verbal_quiz_start(request):
    if 'selected_questions' not in request.session:
        question_ids = list(Cognitive_NVI_Questions_Dataset.objects.values_list('NVI_IMAGE_QUESTION_ID', flat=True))
        selected_questions = random.sample(question_ids, 30) if len(question_ids) >= 30 else question_ids
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

    if request.method == 'POST':
        selected_option = request.POST.get('option')
        cognitive_assessment_id = request.session.get('cognitive_assessment_id')

        if cognitive_assessment_id and selected_option:
            cognitive_assessment = Cognitive_Assessment.objects.get(COGNITIVE_ASSESSMENT_ID=cognitive_assessment_id)
            is_correct = selected_option == question.ANSWERS

            Cognitive_NVI_Answers_Dataset.objects.create(
                COGNITIVE_ASSESSMENT_ID=cognitive_assessment,
                NVI_IMAGE_QUESTION_ID=question,
                JOB_SEEKER_ANS=selected_option,
                IS_CORRECT=is_correct
            )

        if next_question_index is not None:
            return redirect('non_verbal_quiz', question_index=next_question_index)
        else:
            return redirect('phase_two_completed')

    options = [
        question.OPTION1.strip(), question.OPTION2.strip(),
        question.OPTION3.strip(), question.OPTION4.strip(),
        question.OPTION5.strip(), question.OPTION6.strip(),
        question.OPTION7.strip(), question.OPTION8.strip()
    ]

    # Filter out options that are "NONE"
    options = [option for option in options if option and option != "nan"]

    context = {
        'question': question,
        'next_question_index': next_question_index,
        'total_questions': len(selected_questions),
        'options': options,
    }

    return render(request, 'non_verbal_quiz/non_verbal_quiz.html', context)


def non_verbal_quiz_start_redirect(request):
    return redirect('non_verbal_quiz_start')
# --------------------------------[ ENDS ]---------------------------------------------------


# ----------------------------[ TECHNICAL QUIZ ]---------------------------------------------
def technical_quiz_start(request):
    if 'selected_technical_questions' not in request.session:
        question_ids = list(Technical_Questions_Dataset.objects.values_list('TECH_ID', flat=True))
        selected_questions = random.sample(question_ids, 30) if len(question_ids) >= 30 else question_ids
        request.session['selected_technical_questions'] = selected_questions
    return redirect('technical_quiz', question_index=0)

def technical_quiz(request, question_index=0):
    selected_questions = request.session.get('selected_technical_questions', [])
    
    if not selected_questions:
        return redirect('technical_quiz_start')

    question_id = selected_questions[question_index]
    question = get_object_or_404(Technical_Questions_Dataset, TECH_ID=question_id)
    next_question_index = question_index + 1 if question_index < len(selected_questions) - 1 else None

    if request.method == 'POST':
        selected_option = request.POST.get('option')
        technical_assessment_id = request.session.get('technical_assessment_id')

        if technical_assessment_id and selected_option:
            technical_assessment = Technical_Assessment.objects.get(TECHNICAL_ASSESSMENT_ID=technical_assessment_id)
            is_correct = selected_option == question.ANSWER

            Technical_Answers_Dataset.objects.create(
                TECHNICAL_ASSESSMENT_ID=technical_assessment,
                TECH_ID=question,
                JOB_SEEKER_ANS=selected_option,
                IS_CORRECT=is_correct
            )

        if next_question_index is not None:
            return redirect('technical_quiz', question_index=next_question_index)
        else:
            return redirect('phase_three_completed')

    options = [
        question.A.strip(), question.B.strip(),
        question.C.strip(), question.D.strip()
    ]

    context = {
        'question': question,
        'next_question_index': next_question_index,
        'total_questions': len(selected_questions),
        'options': options,
    }

    return render(request, 'technical_quiz/technical_quiz.html', context)


def technical_quiz_start_redirect(request):
    return redirect('technical_quiz_start')
# -------------------------------[ ENDS ]-----------------------------------------------------


# ----------------------------[ PHASE COMPLETETIONS ]-----------------------------------------
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
# ------------------------------------[ ENDS ]-----------------------------------------------
