from .models import SiteSettings


def site_settings(request):
    settings = SiteSettings.load()
    return {
        'text_obfuscation_enabled': settings.text_obfuscation_enabled,
    }
