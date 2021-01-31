from django.conf import settings
from django.contrib.auth import logout as logout_func
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.models import AuthToggle,PassPhrase

def register(request):
    if request.method == "POST":
        # Get form values
        # first_name = request.POST['first_name']
        # last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if passwords match
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken.')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(
                        request, 'That email is already being used.')
                    return redirect('register')
                else:
                    # approved
                    user = User.objects.create_user(
                        username=username,
                        password=password,
                        email=email,
                        # first_name=first_name,
                        # last_name=last_name
                    )
                    # Login after register
                    ''' auth.login(request, user)
                    messages.success(request, "You are now logged in")
                    return redirect('index')'''
                    user.save()
                    user.success(
                        request, "You are now registered and can now log in")
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


'''
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')
'''

'''def dashboard(request):
    return render(request, 'landings/portal.html')'''

def index(request):
    if request.method == "POST":

        passphrase = request.POST.get('passphrase')
        
        gateway = False

        protection = AuthToggle.objects.first().enable_protection
        
        if passphrase:
            # check for all passphrase values in the database 
            for x in PassPhrase.objects.all().values():
                if passphrase == x['passphrase'] and protection:
                    gateway = True
                    break
        if gateway:        
            return redirect('portal')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'landings/gateway.html')
    else:
        return render(request, 'landings/gateway.html')

def portal(request):
    context = {
        "protection": AuthToggle.objects.first()
    }
    return render(request, 'landings/portal.html', context)

def logout(request):
    return redirect('index')

def pending(request):
    return render(request, 'accounts/pending.html')

def reset(request):
    # used when a user forgets his or her password and chooses a new one
    return render(request, 'accounts/reset.html')
