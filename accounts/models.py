import random
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings

class AuthToggle(models.Model):
    is_protected = models.BooleanField(default=False)
    faravahar = models.BooleanField(default=False)
    nuclear = models.BooleanField(default=True)
    timeout = models.IntegerField(default=1)
    # is_time_session = models.BooleanField(default=False)
    # start_time_session = models.DateTimeField(null=True, blank=True)
    email = models.EmailField(max_length=50, default='')

    def __str__(self):
        return "Options"

class PassPhrase(models.Model):
    passphrase = models.CharField(max_length=100, default="YourMagicPassphrase")

    def __str__(self):
        return self.passphrase
