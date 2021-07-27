from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.signals import user_logged_in
from django.contrib import messages
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

def signIn(sender, user, request, **kwargs):
    try:
        DB_Found = False
        DB_Connected = False
        result = subprocess.run(['heroku', 'pg:info', '--app', 'tarot-prod'], stdout=subprocess.PIPE)
        for (env, url) in os.environ.items():
            if env.startswith('HEROKU_POSTGRESQL'):
                DB_Found = True

                formatted_Data = []

                for formatted_String in str(result.stdout).split('=== '):

                    start_DbName = formatted_String.find("HEROKU_POSTGRESQL_")
                    end_DbName = formatted_String.find("\\nPlan")
                    DbName = formatted_String[start_DbName:end_DbName]


                    start_AddOn = formatted_String.find("Add-on:")
                    end_AddOn = formatted_String.find("\\n\\n")
                    AddOn = formatted_String[start_AddOn:end_AddOn].replace('Add-on:                ', "")

                    formatted_Data.append({
                        "name": DbName.replace(", DATABASE_URL", ""),
                        "addon": AddOn
                    })

                color_DB = getDbName(env)

                current_DB = getDbName('DATABASE_URL')

                for data in formatted_Data:
                    if env == data['name'] and color_DB == current_DB:
                        DB_Connected = True
                        messages.add_message(request, messages.SUCCESS, data['name'] + " / " + data['addon'])
                
        if not DB_Found :
            messages.add_message(request, messages.WARNING, "Currently there is no database set to DATABASE_URL")
        elif not DB_Connected :
            messages.add_message(request, messages.WARNING, "Currently you are running app on localhost")
    except:
        messages.add_message(request, messages.ERROR, "Currently there is no database found")


user_logged_in.connect(signIn)