from django.template.defaultfilters import slugify
from django.db import models
from generators.models import Generator


class EssayArticle(models.Model):
    DEFAULT_KEY = 1

    title = models.CharField(max_length=256)
    web_address = models.CharField(max_length=256)
    web_address_slug = models.SlugField(blank=True, max_length=512)
    is_published = models.BooleanField(default=True)
    content = models.TextField(blank=True)
    biblio = models.name = models.ForeignKey(
        'essays.BibliographyArticle', related_name="essay_biblio",
        default=DEFAULT_KEY, blank=True, null=True,
        on_delete=models.SET_NULL
    )
    content_changes_logged = models.ForeignKey(
        'essays.ContentChanges', related_name="essay_content_changes",
        default=DEFAULT_KEY, blank=True, null=True,
        on_delete=models.SET_NULL
    )
    is_published = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.web_address_slug:
            self.web_address_slug = slugify(self.web_address)

        super(EssayArticle, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class CuratedWatchtower(models.Model):
    DEFAULT_KEY = 1

    title = models.CharField(max_length=256)
    introduction = models.TextField(blank=True)
    conclusion = models.TextField(blank=True)
    content_changes_logged = models.ForeignKey(
        'essays.ContentChanges', related_name='watchower_content_changes',
        default=DEFAULT_KEY, blank=True, null=True,
        on_delete=models.SET_NULL)
    biblio = models.ForeignKey(
        'essays.BibliographyArticle', related_name="watchower_biblio",
        default=DEFAULT_KEY, blank=True, null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.title


class CuratedSlashdot(models.Model):
    DEFAULT_KEY = 1

    title = models.CharField(max_length=256)
    introduction = models.TextField(blank=True)
    conclusion = models.TextField(blank=True)
    content_changes_logged = models.ForeignKey(
        'essays.ContentChanges', related_name='slashdot_content_changes',
        default=DEFAULT_KEY, blank=True, null=True,
        on_delete=models.SET_NULL
    )
    biblio = models.ForeignKey(
        'essays.BibliographyArticle', related_name='slashdot_biblio',
        default=DEFAULT_KEY, blank=True, null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title


class ContentChanges(models.Model):
    title = models.CharField(max_length=256)
    content_changes_logged = models.TextField(
        blank=True, help_text="Please use line space for bullet points")

    def __str__(self):
        return self.title

    def log_to_bullets(self):
        return self.content_changes_logged.split('\r\n')


# ContentChanges(models.Model).log_to_bullets(self)


class ObjectionsArticle(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField(blank=True)

    def __str__(self):
        return self.title


class BibliographyArticle(models.Model):
    title = models.CharField(max_length=256)
    biblio = models.TextField(blank=True)

    def __str__(self):
        return self.title

    def biblio_into_bullets(self):
        return self.biblio.split('\r\n')
