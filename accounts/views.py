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

SESSION_TIMEOUT = AuthToggle.objects.first()
nuclear = AuthToggle.objects.first()
faravahar = AuthToggle.objects.first()

@login_required
def portal(request):
    context = {
        "protection": AuthToggle.objects.first(),
        "email": AuthToggle.objects.first(),
    }
    return render(request, 'landings/portal.html', context)

class Gateway(LoginView): #,LoginRequiredMixin): #book_form.html
    model = AuthToggle 
    fields = '__all__'
    # form_class = LoginForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    #def get_success_url(self):
    #    return reverse_lazy('/')
    
class EndSession(LogoutView):
    model = AuthToggle
    template_name = 'registration/logged_out.html'
    
