from django.shortcuts import render

# Create your views here.
def start_screen(request):
    return render(request, './start-screen/start_screen.html')

def login(request):
    return render(request, './login/login.html')