from django.contrib.auth.decorators import login_required
from functools import wraps
from .models import *
from django.db import DatabaseError
from django.shortcuts import render, redirect
from django.urls import reverse


# I am using this custom decorator to handle redirect request after logging in.
def protected_redirect(view_func):

    def wrapper(request, *args, **kwargs):
        auth_toggle = AuthToggle.objects.first()
        if auth_toggle and auth_toggle.is_protected:
            if not request.user.is_authenticated:
                return redirect('index')
            # elif not request.user.is_staff:
            #     return redirect('portal')
        return view_func(request, *args, **kwargs)
    return wrapper