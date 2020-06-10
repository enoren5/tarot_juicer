from django.contrib import admin
from .models import EssayArticle, CuratedSlashdot, CuratedWatchtower, ContentChanges, ObjectionsArticle, BibliographyArticle


class EssayArticleAdmin(admin.ModelAdmin):
    ''' 
    The guide I followed to implement this classinstance is from 
    Brad Traversy’s BT Real Estate course on Udemy: Section 6, 
    Video 39
    '''
    list_display = ('title', 'web_address', 'is_published',)
    list_display_links = ('title',)
    search_fields = ('content',)
    raw_id_fields = ('content_changes_logged', 'biblio',)
    list_editable = ('is_published',)


class CuratedWatchtowerAdmin(admin.ModelAdmin):
    ''' 
    The guide I followed to implement this classinstance is from 
    Brad Traversy’s BT Real Estate course on Udemy: Section 6, 
    Video 39
    '''
    list_display = ('title',)
    list_display_links = ('title',)
    search_fields = ('introduction', 'conclusion',)
    raw_id_fields = ('content_changes_logged', 'biblio',)


class CuratedSlashdotAdmin(admin.ModelAdmin):
    ''' 
    The guide I followed to implement this classinstance is from 
    Brad Traversy’s BT Real Estate course on Udemy: Section 6, 
    Video 39
    '''
    list_display = ('title',)
    list_display_links = ('title',)
    search_fields = ('introduction', 'conclusion',)
    raw_id_fields = ('content_changes_logged', 'biblio')


admin.site.register(EssayArticle, EssayArticleAdmin)
admin.site.register(CuratedSlashdot, CuratedSlashdotAdmin)
admin.site.register(CuratedWatchtower, CuratedWatchtowerAdmin)
admin.site.register(ContentChanges)
admin.site.register(ObjectionsArticle)
admin.site.register(BibliographyArticle)
