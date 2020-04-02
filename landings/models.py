from django.db import models

# Create your models here.


class EssayList(models.Model):
    text_content = models.TextField(blank=True)

    '''def __str__(self):
        return self.title'''


class AboutContent(models.Model):
    text_content = models.TextField(blank=True)

    '''def __str__(self):
        return self.title'''
