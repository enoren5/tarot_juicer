import random
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings

class AuthToggle(models.Model):
    On = models.BooleanField(default=False)
    swap_html = models.BooleanField(default=False)
    nuclear = models.BooleanField(default=True)
    timeout = models.IntegerField(default=1)

    def __str__(self):
        return "Options"

class PassPhrase(models.Model):
    passphrase = models.CharField(max_length=100, default="YourMagicPassphrase")

    def __str__(self):
        return self.passphrase