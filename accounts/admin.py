from django.contrib import admin

# Register your models here.
from accounts.models import AuthToggle, PassPhrase, Email

admin.site.register(AuthToggle)
admin.site.register(PassPhrase)
admin.site.register(Email)