from django.contrib import admin
from .models import FooterAddress, SiteSettings


@admin.register(FooterAddress)
class FooterAddressAdmin(admin.ModelAdmin):
    list_display = ('text',)
    ordering = ('id',)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('text_obfuscation_enabled',)
    
    fieldsets = (
        ('Text Protection', {
            'fields': ('text_obfuscation_enabled',),
            'description': 'Configure text obfuscation settings for essays, generators, and landings pages.'
        }),
    )
    
    def has_add_permission(self, request):
        if SiteSettings.objects.exists():
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        return False
