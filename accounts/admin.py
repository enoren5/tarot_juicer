from django.contrib import admin

# Register your models here.
from accounts.models import AuthToggle

admin.site.register(AuthToggle)