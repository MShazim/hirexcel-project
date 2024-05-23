from django.shortcuts import render

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
