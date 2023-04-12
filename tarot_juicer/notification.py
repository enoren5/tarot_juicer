from django.contrib import messages
import subprocess
import os

def getDbName(environment):
    url = os.environ.get(environment)
    start = url.find("://") + 3
    end = url.find("@") - 1
    return url[start:end].split(':')[0]

def run_command():
    try:
        return subprocess.run(['heroku', 'pg:info', '--app', 'tarot-prod'], stdout=subprocess.PIPE)
    except:
        return subprocess.run(['heroku', 'pg:info', '--app', 'tarot-prod'], shell=True, stdout=subprocess.PIPE)

def message_check_db(request, **kwargs):
    try:

        DB_Found = False
        DB_Connected = False
        result = run_command()
        print("\n RESULT  :", result)
        for (env, url) in os.environ.items():
            if env.startswith('HEROKU_POSTGRESQL'):
                DB_Found = True
                print("\n FOUND DB :", DB_Found)

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
            print("\n DB NOT FOUND :", DB_Found)
            messages.add_message(request, messages.WARNING, "Currently there is no database set to DATABASE_URL")
        elif not DB_Connected :
            messages.add_message(request, messages.WARNING, "Currently you are running app on localhost")
    except:
        messages.add_message(request, messages.ERROR, "Currently there is no database found")

def message_warn_admin_access(request, **kwargs):
    messages.add_message(request, messages.WARNING, "Admin Only Access")

def messages_print(case, message):

    switch = {
        'error': '\033[91m\n' + message + '\033[0m\n',
        'success': '\033[92m\n' + message + '\033[0m\n',
        'warning': '\033[93m\n' + message + '\033[0m\n',
        'info': '\033[94m\n' + message + '\033[0m\n'
    }

    print(switch.get(case))
