from django.contrib import admin
from .models import Generator


class GenerateAdmin(admin.ModelAdmin):
    ''' 
    The guide I followed to implement this classinstance is from 
    Brad Traversy’s BT Real Estate course on Udemy: Section 6, 
    Video 39
    '''
    list_display = ('title', 'number', 'hebrew_letter',
                    'watchtower_position', 'slashdot_position',)
    list_display_links = ('title', 'number',)
    list_filter = ('watchtower_position', 'slashdot_position',)
    search_fields = ('description', 'st_paul_content',
                     'f_loss_content', 'galileo_content')

    raw_id_fields = ('content_changes_logged', 'biblio')


admin.site.register(Generator, GenerateAdmin)
