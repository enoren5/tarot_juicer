from django.db import models

# Create your models here.


class EssayList(models.Model):
    title = models.CharField(max_length=256, default='Essay list')
    # is_published = models.BooleanField(default=True)
    text_content = models.TextField(blank=True)
        
    def __str__(self):
        return self.title


class AboutContent(models.Model):
    title = models.CharField(max_length=256, default='What is going on here?')
    # is_published = models.BooleanField(default=True)
    text_content = models.TextField(blank=True)
        
    def __str__(self):
        return self.title

class HowTo(models.Model):
    title = models.CharField(max_length=256, default='How to use this website')
    # is_published = models.BooleanField(default=True)
    text_content = models.TextField(blank=True)
    
    def __str__(self):
        return self.title