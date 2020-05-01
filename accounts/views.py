from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.


def register(request):
    if request.method == "POST":
        messages.error(request, 'Testing error')
        return redirect('register')
        ''' # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if passwords match
        if password == password2:
            return
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')'''
    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.method == "POST":
        # Login User
        return
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    return redirect(request, 'index')


def dashboard(request):
    return render(request, 'accounts/dashboard.html')


def gateway(request):
    return render(request, 'landings/gateway.html')
