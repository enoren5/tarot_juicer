from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from accounts.models import AuthToggle, PassPhrase
from . import notification
from django.conf import settings

global protected_paths

protected_paths = [reverse('portal')]

messageSent = False

REPEATING_PATH = ""

def IS_PATH_REPEATING(request):
    global REPEATING_PATH
    
    if request.path != REPEATING_PATH:
        REPEATING_PATH = request.path
        return False
    else:
        return True

def authentication_middleware(get_response):
    def middleware(request):
        global protected_paths, messageSent, IS_PATH_REPEATING

        auth_toggle = AuthToggle.objects.first()
        swap_html = AuthToggle.objects.first()
        nuclear = AuthToggle.objects.first()
        isLoggedIn = request.user.is_authenticated

        # Exception if auth_toggle is not present then create one with a default value
        if auth_toggle:
            pass
        else:
            auth = AuthToggle.objects.create(enable_protection = False) 
            auth.save()

        # Exception if swap_html is not present then create one with a default value
        if swap_html:
            swap_html = swap_html.swap_html
        else:
            swap_html = AuthToggle.objects.create(swap_html = False) 
            swap_html.save()

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
            "swap_html": swap_html,
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
                    if request.POST.get('passphrase') == x['passphrase'] and auth_toggle.enable_protection:
                        protected_paths = []
                        break
                # if protection is checked and if logout is clicked then revert changes and serve only gateway
                if request.path.startswith(reverse('logout')) and auth_toggle.enable_protection:
                    protected_paths = [reverse('portal')]
                elif not auth_toggle.enable_protection:
                    protected_paths = []

                # if protection is not checked serve portal
                if not auth_toggle.enable_protection and request.path in unprotected_paths and not admin_path:
                    return render(request, 'landings/portal.html', context)
                else: # else serve gateway
                    if request.path in protected_paths and not admin_path:
                        return render(request, 'landings/gateway.html', context) 


        response = get_response(request)

        return response

    return middleware