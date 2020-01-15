from django.contrib import admin
from .models import EssayArticle, CuratedSlashdot, CuratedWatchtower, ContentChanges
# Register your models here.

admin.site.register(EssayArticle)
admin.site.register(CuratedSlashdot)
admin.site.register(CuratedWatchtower)
admin.site.register(ContentChanges)
