from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

def create_user_if_not_exists():
    if not User.objects.filter(username=settings.AUTHENTICATED_VISITOR_USERNAME).exists():
        User.objects.create_user(username=settings.AUTHENTICATED_VISITOR_USERNAME,
                            email=settings.AUTHENTICATED_VISITOR_USERNAME,
                            password=settings.AUTHENTICATED_VISITOR_PASSWORD)

class AuthToggle(models.Model):
    active = models.BooleanField(default=True)

class PassPhrase(models.Model):
    passphrase = models.CharField(max_length=100, default="YourMagicPassphrase")
    
    def __str__(self):
        return self.passphrase