from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from patient.models import Doctor

def doctor_login(request):
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a success page
        else:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'login.html')
    
    return render(request, 'login.html')


def doctor_logout(request):
    logout(request)
    return redirect('login')  # Redirect to the login page