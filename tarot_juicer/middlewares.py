from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from accounts.models import AuthToggle, PassPhrase
from . import notification
from django.conf import settings

from datetime import datetime, timedelta
from django.contrib import auth
from tarot_juicer.urls import urlpatterns as tarot_urls
from landings.urls import urlpatterns as landing_urls
from generators.urls import urlpatterns as generator_urls
from essays.urls import urlpatterns as essay_urls
from accounts.urls import urlpatterns as account_urls

global protected_paths
print("Ist Print")

protected_paths = [reverse('portal')]

messageSent = False

REPEATING_PATH = ""

print("2nd print before is path repeating")
def IS_PATH_REPEATING(request):
    global REPEATING_PATH

    if request.path != REPEATING_PATH:
        REPEATING_PATH = request.path
        return False
    else:
        return True
print("3rd print before add protected paths")
def ADD_PROTECTED_PATH():
    print("4th print")
    global protected_paths

    # Paths that should be protected
    protected_paths = [
        # reverse('portal'),
        # reverse('slashdot'),
        # reverse('watchtower'),
        # reverse('objections'),
        # reverse('content_changelog'),
        # reverse('bibliography'),
        # reverse('all_content_dump'),
        # reverse('about'),
        # reverse('essay_list'),
        # reverse('stewart_mortenson_runyon'),
        # reverse('run_forrest_run'),
        # reverse('amerika'),
        tarot_urls, essay_urls,generator_urls, landing_urls, account_urls
    ]

def authentication_middleware(get_response):

    def middleware(request):
        global protected_paths, messageSent, IS_PATH_REPEATING, ADD_PROTECTED_PATH

        auth_toggle = AuthToggle.objects.first()
        faravahar = AuthToggle.objects.first()
        nuclear = AuthToggle.objects.first()
        isLoggedIn = request.user.is_authenticated


        # Exception if auth_toggle is not present then create one with a default value
        if auth_toggle:
            pass
                
        else:
            auth = AuthToggle.objects.create(is_protected = False) 
            auth.save()

        # Exception if faravahar is not present then create one with a default value
        if faravahar:
            faravahar = faravahar.faravahar
        else:
            faravahar = AuthToggle.objects.create(faravahar = False) 
            faravahar.save()

        # Exception if nuclear is not present then create one with a default value
        if nuclear:
            nuclear = nuclear.nuclear
        else:
            nuclear = AuthToggle.objects.create(nuclear = False) 
            nuclear.save()

        admin_path = request.path.startswith(reverse('admin:index'))


        unprotected_paths = [
            reverse('index'),
        ]


        context = {
            "faravahar": faravahar,
            "nuclear": nuclear,
            "protection": AuthToggle.objects.first()
        }

        IS_LOGIN_PATH = settings.ADMIN_PATH + 'login'

        IS_LOGOUT_PATH = settings.ADMIN_PATH + 'logout'


        if IS_LOGIN_PATH in request.path and not messageSent:
            notification.message_check_db(request)
            messageSent = True
        elif IS_LOGOUT_PATH in request.path and messageSent:
            messageSent = False

        if nuclear:
            if isLoggedIn :
                if not admin_path:
                    if not IS_PATH_REPEATING(request):
                        notification.message_warn_admin_access(request)
                else:
                    pass
            else:
                if not admin_path:
                    return render(request, 'landings/gateway.html', context)
        else:
            if auth_toggle :
                
                    
                # if protection is checked and passphrase is entered then serve the portal otherwise serve gateway
                for x in PassPhrase.objects.all().values():
                    print("Values of phrases", x)
                    if request.POST.get('passphrase') == x['passphrase'] and auth_toggle.is_protected:
                        protected_paths = []
                        break
                    else:
                        ADD_PROTECTED_PATH()
                        
                # if protection is checked and if logout is clicked then revert changes and serve only gateway
                if request.path.startswith(reverse('logout')) and auth_toggle.is_protected:
                    ADD_PROTECTED_PATH()
                elif not auth_toggle.is_protected:
                    protected_paths = []


                # if protection is not checked serve portal
                if not auth_toggle.is_protected and request.path in unprotected_paths and not admin_path:
                    return render(request, 'landings/portal.html', context)
                else: # else serve gateway
                    if request.path in protected_paths and not admin_path:
                        return render(request, 'landings/gateway.html', context)

        response = get_response(request)

        return response

    return middleware

def autologout_middleware(get_response):
    def middleware(request):
        response = get_response(request)

        isLoggedIn = request.user.is_authenticated

        SESSION_TIMEOUT = AuthToggle.objects.first()
        admin_path = request.path.startswith(reverse('admin:index'))

        if not isLoggedIn:

            try:

                if datetime.now() - request.session['last_touch'] > timedelta( 0, SESSION_TIMEOUT.timeout * 60, 0):

                    ADD_PROTECTED_PATH()

                    del request.session['last_touch']

                    del request.session['loggedIn']

                    notification.messages_print('error', 'Session timeout at: ' + request.path)

                    request.session['last_page_visited'] = request.path
                        
                    return redirect('/')

                else:
                    notification.messages_print('success', 'Passed session validation')

            except KeyError:
                pass
                

            if not request.session.has_key('last_touch') and request.session.has_key('loggedIn'):

                request.session['last_touch'] = datetime.now()

                notification.messages_print('info', 'New session of ' + str(SESSION_TIMEOUT.timeout) + ' minutes has started')
                print("New session started")
                

        else:
            notification.messages_print('warning', 'Admin access detected')
            print("Admin")

        return response

    return middleware
