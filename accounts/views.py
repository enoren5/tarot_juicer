from django.conf import settings
from django.contrib.auth import logout as logout_func
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.models import AuthToggle,PassPhrase
from tarot_juicer import notification
import time
import threading
from django.contrib.auth.decorators import login_required

# from tarot_juicer.urls import urlpatterns as tarot_urls
from landings.urls import urlpatterns as landing_urls
from generators.urls import urlpatterns as generator_urls
from essays.urls import urlpatterns as essay_urls
from . import urls as account_urls

from datetime import datetime, timedelta


def ADD_PROTECTED_PATH():
    global protected_paths

    # Paths that should be protected
    protected_paths = [
        essay_urls, generator_urls, landing_urls, account_urls
    ]

SESSION_TIMEOUT = AuthToggle.objects.first()
nuclear = AuthToggle.objects.first()
faravahar = AuthToggle.objects.first()



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

global attempts, maxAttempts, enableTimer
attempts = 0
maxAttempts = 10
enableTimer = False



def middleware(request):
        SESSION_TIMEOUT = AuthToggle.objects.first()
        nuclear = AuthToggle.objects.first()
        faravahar = AuthToggle.objects.first()
        isLoggedIn = request.user.is_authenticated
        username = request.POST['username']
        password = request.POST['password']
        # if someone is trying to acces admin url then ignore all token/passphrase procedure
        # if request.path.startswith("/admin"):
        #     response = get_response(request)
        #     return response

        if request.method == "POST":
            if username and password:
                # check for all passphrase values in the database
                # for x in PassPhrase.objects.all().values():
                #     if passphrase == x['passphrase'] and protection and not enableTimer:
                #         gateway = True
                        # request.session['loggedIn'] = True
                        # print("\n Logged in Session Index View \n", request.session['loggedIn'])
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    auth.login(request, user)
                    print("\n User in middleware view :", user)
                    request.session['last_touch'] = datetime.now()
                    request.session['loggedIn'] = True
                    messages.success(request, 'You are now logged in!')
            # for x in PassPhrase.objects.all().values():
            #     if request.POST.get('passphrase') == x['passphrase']:
            #         auth = AuthToggle.objects.get_or_create(is_protected=True)
                    # request.session['auth_token'] = auth
                    # request.session['last_touch'] = datetime.now()
                    # request.session['loggedIn'] = True
                    # print("\n Logged in Session middleware \n", request.session['loggedIn'])

                    notification.messages_print(
                        'info', 'New session of ' + str(SESSION_TIMEOUT.timeout) + ' minutes has started')
                    return redirect('portal')
        else:  # auth_token means check if user has auth_token and if it is valid, allow them to access the route
            try:
                if username and password:
                    if datetime.now() - request.session.get('last_touch',datetime.now()) > timedelta( 0, SESSION_TIMEOUT.timeout * 60, 0):
                        ADD_PROTECTED_PATH()

                        del request.session['last_touch']

                        del request.session['loggedIn']
                        # del request.session['auth_token']
                        notification.messages_print(
                            'error', 'Session timeout at: ' + request.path)

                        request.session['last_page_visited'] = request.path

                        return HttpResponseRedirect('/')
                        # when a user clicks on Home button, auth token will be deleted and user will have to pass the passphrase again
                    elif SESSION_TIMEOUT.is_protected == True:
                        if request.session['loggedIn']:
                            if request.path == '/':
                                ADD_PROTECTED_PATH()
                                del request.session['loggedIn']
                                notification.messages_print(
                                'error', 'Session deleted at: ' + request.path)
                                return redirect('/')

                    else:
                        notification.messages_print('success', 'Passed session validation')
                elif request.path != '/':
                    if SESSION_TIMEOUT.is_protected:
                        return HttpResponseRedirect('/')
                    else:
                        pass
                elif username is None:
                    print("\n Username - Redirect to home :", username)
                    if not request.session.get('loggedIn'):
                        if request.path !='/':
                            return HttpResponseRedirect('/')
                else: # pass phrase is not provided, it will redirect to protected gateway
                    if SESSION_TIMEOUT.is_protected and not SESSION_TIMEOUT.nuclear and not SESSION_TIMEOUT.faravahar:
                        if request.path != "/":
                            print("\n path !=/ - Redirect to home :")
                            return HttpResponseRedirect('/')
                        else:
                            pass
                            # print("Checking Admin only access")
                            # notification.message_warn_admin_access(request)
                            # return render(request, 'landings/portal.html', context)
                    else:
                        pass
                    if SESSION_TIMEOUT.nuclear == True and SESSION_TIMEOUT.is_protected == True:
                        if request.path == '/':
                            return redirect('portal')


            except KeyError:
                print("\n Except :")
        # response = get_response(request)
        # return response


def index(request):
    auth_toggel = AuthToggle.objects.first().faravahar
    faravahar = AuthToggle.objects.first().faravahar
    nuclear = AuthToggle.objects.first().nuclear
    context = {
        "faravahar": faravahar,
        "nuclear": nuclear,
    }
    if not nuclear:
        if request.method == "POST":
            passphrase = request.POST.get('passphrase')
            gateway = False
            protection = AuthToggle.objects.first().is_protected # this means protection is turned On
            global attempts, maxAttempts, enableTimer
            username = request.POST['username']
            password = request.POST['password']
            if username and password:
                # check for all passphrase values in the database
                # for x in PassPhrase.objects.all().values():
                #     if passphrase == x['passphrase'] and protection and not enableTimer:
                #         gateway = True
                        # request.session['loggedIn'] = True
                        # print("\n Logged in Session Index View \n", request.session['loggedIn'])
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    # auth.login(request, user)
                    # print("\n User in Index view :", user)
                    middleware(request)
                    messages.success(request, 'You are now logged in!')
                    return redirect('portal')
                    # break
            if gateway:
                if request.session.has_key('last_page_visited'):
                    resumed_path = request.session['last_page_visited']
                    notification.messages_print('warning', "Resuming Session At: " + resumed_path)
                    del request.session['last_page_visited']
                    return HttpResponseRedirect(resumed_path)
                return redirect('portal')
            else:
                attempts += 1

                def start_timeout():
                    global attempts, enableTimer
                    messages.error(request, 'Timeout Reached: you had attempted ' + str(attempts) + " attempts please wait 1 hour to continue")
                    # Time in seconds
                    time.sleep(3600) # 3600 seconds = 1 hr, 60 seconds = 1 min
                    attempts = 0
                    enableTimer = False

                t1 = threading.Thread(target=start_timeout)

                if attempts >= maxAttempts and not enableTimer:
                    t1.start()
                    enableTimer = True
                elif enableTimer:
                    messages.error(request, 'Timeout Reached: please wait 1 hour to continue')
                else:
                    messages.error(request, 'Invalid credentials. Attempts left: ' + str(maxAttempts - attempts))
                return render(request, 'landings/gateway.html', context)
        else:
            return render(request, 'landings/gateway.html', context)
    else :
        return render(request, 'landings/gateway.html', context)



def portal(request):
    context = {
        "protection": AuthToggle.objects.first(),
        "email": AuthToggle.objects.first(),
    }
    return render(request, 'landings/portal.html', context)


def reentry(request):
    context = {
        "protection": AuthToggle.objects.first()
    }
    return render(request, 'landings/reentry.html', context)



def logout(request):
    global attempts
    attempts = 0
    del request.session['loggedIn']
    del request.session['auth_token']
    notification.messages_print(
                            'error', 'Session loggedout at: ' + request.path)
    return redirect('/')


def pending(request):
    return render(request, 'accounts/pending.html')


def reset(request):
    # used when a user forgets his or her password and chooses a new one
    return render(request, 'accounts/reset.html')




def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in!')
            return redirect('portal')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


'''def dashboard(request):
    return render(request, 'landings/portal.html')'''
