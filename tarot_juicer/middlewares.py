from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from accounts.models import get_random_visitor_name
from accounts.models import AuthToggle

def authentication_middleware(get_response):
    def middleware(request):
        auth_toggle = AuthToggle.objects.first()
        if auth_toggle:
            pass
        else:
            auth = AuthToggle.objects.create(active = False) 
            auth.save()

        if auth_toggle :
            if auth_toggle.active and (reverse('index') != None):  # authentication NOT required
                if not request.user.is_superuser and request.path == reverse('index') and request.user.is_authenticated and request.session.has_key('username') and request.session.has_key('authy'):
                    if request.session['authy']:
                        u_name = request.session['username']
                        return redirect('portal', user_name=u_name)
            else:  # authentication required
                if request.user.is_authenticated and \
                        request.path not in [reverse('index'), reverse('register')] and \
                        not request.path.startswith(reverse('admin:index')) and not auth_toggle.active:
                    return render(request, 'landings/gateway.html')

        response = get_response(request)

        return response

    return middleware
