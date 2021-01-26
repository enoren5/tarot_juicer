from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from accounts.models import AuthToggle

def authentication_middleware(get_response):
    def middleware(request):
        auth_toggle = AuthToggle.objects.first()
        if auth_toggle:
            pass
        else:
            auth = AuthToggle.objects.create(enable_protection = False) 
            auth.save()

        response = get_response(request)

        return response

    return middleware