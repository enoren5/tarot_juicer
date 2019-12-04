from django.db import models
from essays.models import EssayArticle  # CuratedSlashdot, CuratedStPaul


class Generator(models.Model):
    title = models.CharField(max_length=24)
    number = models.IntegerField()
    # tarot_card_image must be an html box to contain a URL reference because the image data must be delegated/outsourced to imgur to save on bandwidth rather than serving the tarot_card_image data locally
    tarot_card_image = models.CharField(max_length=1024)
    astrological = models.CharField(max_length=140)
    alchemical = models.CharField(max_length=140)
    intelligence = models.CharField(max_length=140)
    hebrew_letter = models.CharField(max_length=140)
    letter_meaning = models.CharField(max_length=140)
    description = models.TextField(blank=True)
    galileo_content = models.TextField(blank=True)
    f_loss_content = models.TextField(blank=True)
    st_paul_content = models.TextField(blank=True)

    def __str__(self):
        return self.title
