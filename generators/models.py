from django.db import models
# from essays.models import EssayArticle  # CuratedSlashdot, CuratedStPaul'''


class Generator(models.Model):
    DEFAULT_KEY = 1

    title = models.CharField(max_length=24)
    number = models.IntegerField()
    # tarot_card_image must be an html CharField to contain a URL reference because the image data must be delegated/outsourced to imgur to save on bandwidth rather than serving the tarot_card_image data locally
    tarot_card_image = models.CharField(max_length=1024)
    tarot_card_thumbnail = models.ImageField(upload_to='thumbnails/')
    astrological = models.CharField(max_length=140)
    alchemical = models.CharField(max_length=140)
    intelligence = models.CharField(max_length=140)
    hebrew_letter = models.CharField(max_length=140)
    letter_meaning = models.CharField(max_length=140)
    watchtower_position = models.IntegerField(blank=True, null=True)
    slashdot_position = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True)
    description_bullets = models.TextField(
        blank=False, help_text="Please use line space for bullet points", null=True)
    galileo_content = models.TextField(blank=True)
    galileo_bullets = models.TextField(
        blank=True, help_text="Please use line space for bullet points")
    f_loss_content = models.TextField(blank=True)
    f_loss_bullets = models.TextField(
        blank=True, help_text="Please use line space for bullet points")
    st_paul_content = models.TextField(blank=True)
    st_paul_bullets = models.TextField(
        blank=True, help_text="Please use line space for bullet points")
    content_changes_logged = models.ForeignKey(
        'essays.ContentChanges', related_name='content_changes',
        on_delete=models.SET_NULL, blank=True, null=True,
        default=DEFAULT_KEY
    )
    biblio = models.ForeignKey(
        'essays.BibliographyArticle', related_name='bibliography',
        on_delete=models.SET_NULL, blank=True, null=True,
        default=DEFAULT_KEY
    )

    def description_to_bullet(self):
        if '\r\n' in self.description_bullets:
            break_point = '\r\n'
        else:
            break_point = '\n'
        return self.description_bullets.split(break_point)

    def paul_to_bullet(self):
        if '\r\n' in self.description_bullets:
            break_point = '\r\n'
        else:
            break_point = '\n'
        return self.st_paul_bullets.split(break_point)

    def galileo_to_bullet(self):
        if '\r\n' in self.description_bullets:
            break_point = '\r\n'
        else:
            break_point = '\n'
        return self.galileo_bullets.split(break_point)

    def f_loss_to_bullet(self):
        if '\r\n' in self.description_bullets:
            break_point = '\r\n'
        else:
            break_point = '\n'
        return self.f_loss_bullets.split(break_point)

    def __str__(self):
        return self.title
