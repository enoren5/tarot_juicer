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
        tarot_urls, essay_urls, generator_urls, landing_urls, account_urls
    ]

def simple_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        SESSION_TIMEOUT = AuthToggle.objects.first()
        # if someone is trying to acces admin url then ignore all token/passphrase procedure
        if request.path.startswith("/admin"):
            response = get_response(request)
            return response
            
        if request.method == "POST":
            for x in PassPhrase.objects.all().values():
                if request.POST.get('passphrase') == x['passphrase']:
                    auth = AuthToggle.objects.get_or_create(is_protected=True)
                    request.session['auth_token'] = auth
                    request.session['last_touch'] = datetime.now()

                    notification.messages_print(
                        'info', 'New session of ' + str(SESSION_TIMEOUT.timeout) + ' minutes has started')
        else:  # auth_token menas check if user has auth_token and if it is valid if it is valid, allow them to access the route

            if request.session.get('auth_token',None):
                if datetime.now() - request.session.get('last_touch',datetime.now()) > timedelta( 0, SESSION_TIMEOUT.timeout * 60, 0):
                    ADD_PROTECTED_PATH()

                    del request.session['last_touch']

                    del request.session['loggedIn']
                    del request.session['auth_token']
                    notification.messages_print('error', 'Session timeout at: ' + request.path)

                    request.session['last_page_visited'] = request.path

                    return HttpResponseRedirect('/')

                else:
                    notification.messages_print('success', 'Passed session validation')
            else: # pass phrase is not provided, it will redirect to protected gateway
                if request.path != "/":
                    return HttpResponseRedirect('/')
        # for x in PassPhrase.objects.all().values():
        #     if request.POST.get('passphrase') == x['passphrase'] and auth_toggle.is_protected:
        #         protected_paths = []
        #         break
        print(request.session.keys())
        response = get_response(request)
        return response

    return middleware
