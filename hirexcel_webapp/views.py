from django.shortcuts import render , get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import DISC_Questions_Dataset, Cognitive_NVI_Questions_Dataset, Technical_Questions_Dataset , Job_Position_Criteria
import random

# Create your views here.
def start_screen(request):
    return render(request, './start-screen/start_screen.html')

def jobseeker_login(request):
    return render(request, './login/jobseeker_login.html')

def recruiter_login(request):
    return render(request, './login/recruiter_login.html')

def jobseeker_create_account(request):
    return render(request, './create_account/jobseeker_create_account.html')

def recruiter_create_account(request):
    return render(request, './create_account/recruiter_create_account.html')

def jobseeker_home(request):
    return render(request, './home/jobseeker_home.html')

def recruiter_home(request):
    return render(request, './home/recruiter_home.html')

# def post_job(request):
#     return render(request, './post_job/post_job.html')

def post_job(request):
    if request.method == 'POST':
        # Handle form submission
        job_title = request.POST['jobTitle']
        company_name = request.POST['companyName']
        location = request.POST['location']
        job_type = request.POST['jobType']
        job_position = request.POST['jobPosition']
        job_description = request.POST['jobDescription']
        key_responsibilities = request.POST['keyResponsibilities']
        required_qualifications = request.POST['requiredQualifications']
        required_skills = request.POST['requiredSkills']
        experience_requirements = request.POST['experienceRequirements']
        contact_information = request.POST['contactInformation']
        personality_traits = request.POST.getlist('personalityTraits')
        # Save to database or perform other actions

        # Redirect to a success page or another page
        return redirect('success_page')

    job_positions = Job_Position_Criteria.objects.values_list('JOB_POSITION', flat=True).distinct()
    return render(request, './post_job/post_job.html', {'job_positions': job_positions})

# def get_personality_traits(request):
#     job_position = request.GET.get('job_position')
#     if job_position:
#         criteria = Job_Position_Criteria.objects.filter(JOB_POSITION=job_position)
#         if criteria.exists():
#             personality_traits = set()
#             for criterion in criteria:
#                 if criterion.PERSONALITY_TRAITS and criterion.PERSONALITY_TRAITS.lower() != 'nan':
#                     personality_traits.add(criterion.PERSONALITY_TRAITS)
#                 if criterion.COGNITIVE_SKILLS and criterion.COGNITIVE_SKILLS.lower() != 'nan':
#                     personality_traits.add(criterion.COGNITIVE_SKILLS)
#                 if criterion.EMOTIONAL_INTELLIGENCE and criterion.EMOTIONAL_INTELLIGENCE.lower() != 'nan':
#                     personality_traits.add(criterion.EMOTIONAL_INTELLIGENCE)
#             return JsonResponse({'personality_traits': list(personality_traits)})
#     return JsonResponse({'personality_traits': []})

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

def quiz_start_screen(request):
    return render(request, './quiz/quiz_start_screen.html')

def disc_quiz(request, question_id=1):
    # Get the question based on the current question ID
    question = get_object_or_404(DISC_Questions_Dataset, id=question_id)
    context = {
        'question': question,
        'next_question_id': question_id + 1 if question_id < DISC_Questions_Dataset.objects.count() else None,
        'total_questions': DISC_Questions_Dataset.objects.count()
    }
    return render(request, 'disc_quiz/disc_quiz.html', context)

def non_verbal_quiz(request, question_index=0):
    if 'selected_questions' not in request.session:
        question_ids = list(Cognitive_NVI_Questions_Dataset.objects.values_list('id', flat=True))
        selected_questions = random.sample(question_ids, 30)
        request.session['selected_questions'] = selected_questions
        print(selected_questions)
    else:
        selected_questions = request.session['selected_questions']

    question_id = selected_questions[question_index]
    question = get_object_or_404(Cognitive_NVI_Questions_Dataset, id=question_id)
    next_question_index = question_index + 1 if question_index < 29 else None

    options = [
        question.OPTION1.strip(), question.OPTION2.strip(),
        question.OPTION3.strip(), question.OPTION4.strip(),
        question.OPTION5.strip(), question.OPTION6.strip(),
        question.OPTION7.strip(), question.OPTION8.strip()
    ]

    # Filter out options that are "NONE"
    options = [option for option in options if option and option != "None"]

    context = {
        'question': question,
        'next_question_index': next_question_index,
        'total_questions': len(selected_questions),
        'options': options,
    }

    return render(request, 'non_verbal_quiz/non_verbal_quiz.html', context)


def technical_quiz(request, question_index=0):
    if 'selected_technical_questions' not in request.session:
        question_ids = list(Technical_Questions_Dataset.objects.values_list('id', flat=True))
        selected_questions = random.sample(question_ids, 30)
        request.session['selected_technical_questions'] = selected_questions
    else:
        selected_questions = request.session['selected_technical_questions']

    question_id = selected_questions[question_index]
    question = get_object_or_404(Technical_Questions_Dataset, id=question_id)
    next_question_index = question_index + 1 if question_index < 29 else None

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


def phase_one_completed(request):
    return render(request, './test_complete/phase_one_completed.html')

def phase_two_completed(request):
    return render(request, './test_complete/phase_two_completed.html')

def phase_three_completed(request):
    return render(request, './test_complete/phase_three_completed.html')
