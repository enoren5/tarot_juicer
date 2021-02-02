from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from accounts.models import AuthToggle, PassPhrase

global protected_paths

protected_paths = [reverse('portal')]

def authentication_middleware(get_response):
    def middleware(request):
        global protected_paths

        auth_toggle = AuthToggle.objects.first()

        if auth_toggle:
            pass
        else:
            auth = AuthToggle.objects.create(enable_protection = False) 
            auth.save()

        admin_path = request.path.startswith(reverse('admin:index'))

        unprotected_paths = [
            reverse('index'),
        ]

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
                context = {
                    "protection": AuthToggle.objects.first()
                }
                return render(request, 'landings/portal.html', context)
            else: # else serve gateway
                if request.path in protected_paths and not admin_path:
                    return render(request, 'landings/gateway.html') 

        response = get_response(request)

        return response

    return middleware