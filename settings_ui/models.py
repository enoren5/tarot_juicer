from django.db import models


class FooterAddress(models.Model):
    text = models.TextField(
        help_text="An address or location text to display in the site footer. One entry is chosen at random per page load."
    )

    class Meta:
        verbose_name = "Footer Address"
        verbose_name_plural = "Footer Addresses"

    def __str__(self):
        return self.text[:80]


class SiteSettings(models.Model):
    text_obfuscation_enabled = models.BooleanField(
        default=False,
        help_text="Enable JavaScript-based text obfuscation to prevent copying/selecting text on essays, generators, and landings pages"
    )
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return "Site Settings"
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        pass
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
