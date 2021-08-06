from django.db import models

# Create your models here.


class EssayList(models.Model):
    title = models.CharField(max_length=256, default='Essay list and how to use this website')
    text_content = models.TextField(blank=True)    
    
    def __str__(self):
        return self.title


class AboutContent(models.Model):
    title = models.CharField(max_length=256, default='What is going on here?')
    text_content = models.TextField(blank=True)    
    
    def __str__(self):
        return self.title
