import random
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

global name, password

name = ""
password = ""

def random_visitor_name_generator():
    return "Visitor" + str(random.randint(0,999)) + "-" + str(random.randint(0,9999))

def random_visitor_password_generator():
    return "pass" + str(random.randint(0,999)) + "-" + str(random.randint(0,9999)) + "-" + str(random.randint(0,9999))

def get_random_visitor_name():
    global name
    return name

def get_random_visitor_password():
    global password
    return password

def set_random_visitor_name(data):
    global name
    name = data

def set_random_visitor_password(data):
    global password
    password = data

def create_user_if_not_exists():
    set_random_visitor_name(random_visitor_name_generator())
    set_random_visitor_password(random_visitor_password_generator())
    global name, password
    if not User.objects.filter(username=name).exists():
        User.objects.create_user(username=name, email=name, password=password)

class AuthToggle(models.Model):
    active = models.BooleanField(default=False)

class PassPhrase(models.Model):
    passphrase = models.CharField(max_length=100, default="YourMagicPassphrase")
    
    def __str__(self):
        return self.passphrase