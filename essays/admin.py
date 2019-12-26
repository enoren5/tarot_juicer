from django.contrib import admin
from .models import EssayArticle, CuratedSlashdot, CuratedWatchtower
# Register your models here.

admin.site.register(EssayArticle)
admin.site.register(CuratedSlashdot)
admin.site.register(CuratedWatchtower)
