from django.conf import settings
from django.contrib.auth import logout as logout_func
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from accounts.models import AuthToggle,PassPhrase , create_user_if_not_exists, get_random_visitor_name, get_random_visitor_password

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

    if not request.session.has_key('username'):
        create_user_if_not_exists()
        request.session['username'] = get_random_visitor_name()
    else:
        request.session.clear()

    if request.method == "POST":

        user = None
        passphrase = request.POST.get('passphrase')

        if passphrase:
            # check for all passphrase values in the database 
            for x in PassPhrase.objects.all().values():
                if passphrase == x['passphrase']:
                    user = auth.authenticate(
                            username=get_random_visitor_name(), password=get_random_visitor_password()
                    )
                    break
        else:
            messages.error(request, 'Either you entered an incorrect username and a password combo or incorrect passphrase. Try again.')
            return render(request, 'landings/gateway.html')
        if user:
            auth.login(request, user)
            messages.success(request, 'You are now logged in!')
            authy = AuthToggle.objects.first()
            authy.enable_protection = True
            request.session['authy'] = True
            authy.save()
            if request.session.has_key('username'):
                u_name = request.session['username']
            else:
                u_name = get_random_visitor_name()
            return redirect('portal', user_name=u_name)
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'landings/gateway.html')
    else:
        return render(request, 'landings/gateway.html')

@login_required
def portal(request, user_name):
    if len(user_name) <= 0:
        return render(request, 'landings/gateway.html')
    else:
        return render(request, 'landings/portal.html', {'user_name': user_name})

def logout(request):
    request.session['authy'] = False
    if request.session.has_key('username'):
        u_name = request.session['username']
    else:
        u_name = get_random_visitor_name()
    u = User.objects.get(username=u_name)
    u.delete()
    request.session.clear()
    return redirect('index')

def pending(request):
    return render(request, 'accounts/pending.html')

def reset(request):
    # used when a user forgets his or her password and chooses a new one
    return render(request, 'accounts/reset.html')
