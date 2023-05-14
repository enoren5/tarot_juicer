from django.conf import settings
from django.contrib.auth import logout as logout_func
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.models import AuthToggle,PassPhrase
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView

from django.urls import reverse_lazy
from datetime import timedelta, datetime
from tarot_juicer import notification
from .custom_decorator import protected_redirect

from django.contrib.auth.decorators import user_passes_test

SESSION_TIMEOUT = AuthToggle.objects.first()
nuclear = AuthToggle.objects.first()
faravahar = AuthToggle.objects.first()


@protected_redirect
def portal(request):
    context = {
        "protection": AuthToggle.objects.first(),
        "email": AuthToggle.objects.first(),
    }
    return render(request, 'landings/portal.html', context)

class Gateway(LoginView): # no need to use login required mixin,LoginRequiredMixin): #book_form.html
    model = AuthToggle
    fields = '__all__'
    context_object_name = 'controls'
    # form_class = LoginForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('portal')

    def dispatch(self, request, *args, **kwargs):
        # Overiding the dispatch method to add extra functionality to the loginview
        response = super().dispatch(request, *args, **kwargs)

        auth_toggle = AuthToggle.objects.first()
        if self.request.user.is_authenticated and auth_toggle.is_protected and not request.user.is_staff:
            # It is neccessary to store the time in session to set the session expiry + Start session timer
            request.session['session_start_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            request.session.set_expiry(auth_toggle.timeout * 60) # I am converting the minutes in secconds
            # Print session start time
            notification.messages_print(
                        'info', 'New session of ' + str(SESSION_TIMEOUT.timeout) + ' minutes has started'
                        )
            print(f"Time session started at: {request.session['session_start_time']}")
        elif not self.request.user.is_authenticated and not auth_toggle.is_protected:
            return redirect('portal')
        return response

class EndSession(LogoutView):
    model = AuthToggle
    template_name = 'registration/logged_out.html'

    def dispatch(self, request, *args, **kwargs):
        # this method will redirect the user to login page which is index
        response = super().dispatch(request, *args, **kwargs)
        return redirect('index')

