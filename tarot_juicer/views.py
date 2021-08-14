from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.signals import user_logged_in
from . import notification
import os
import subprocess

def handler404(request, *args, **argv):
    response = render(RequestContext(request), '404.html')
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(RequestContext(request), '500.html')
    response.status_code = 500
    return response

def getDbName(environment):
    url = os.environ.get(environment)
    start = url.find("://") + 3
    end = url.find("@") - 1
    return url[start:end].split(':')[0]

user_logged_in.connect(notification.message_check_db)