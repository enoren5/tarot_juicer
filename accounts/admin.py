from django.contrib import admin

# Register your models here.
from accounts.models import AuthToggle, PassPhrase

admin.site.register(AuthToggle)
admin.site.register(PassPhrase)