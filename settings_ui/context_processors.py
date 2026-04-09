from .models import FooterAddress, SiteSettings


def site_settings(request):
    settings = SiteSettings.load()
    footer_address = FooterAddress.objects.order_by('?').first()
    return {
        'text_obfuscation_enabled': settings.text_obfuscation_enabled,
        'footer_address': footer_address,
    }
