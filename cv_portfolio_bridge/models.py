"""
Mirrors CV_Portfolio's portfolio.* models, which live in the same Postgres
instance as this project. managed=False means this app's migrations never
touch the tables' schema - CV_Portfolio remains the sole owner of that.
Image fields aren't mirrored: their files live on CV_Portfolio's own media
storage, and this content dump has never rendered images (see the `img {
display: none; }` rule in all_content_dump.html).

Used exclusively by essays.views.all_content_dump - these models are not
registered in admin and have no other views pointed at them.
"""

from django.db import models


class Profile(models.Model):
    """Singleton row (pk=1) holding CV_Portfolio's site-wide text sections."""

    name = models.CharField(max_length=120)
    tagline = models.CharField(max_length=200, blank=True)
    preamble_heading = models.CharField(max_length=100, blank=True)
    preamble_text = models.TextField(blank=True)
    time_logger_heading = models.CharField(max_length=100, blank=True)
    time_logger_text = models.TextField(blank=True)
    core_research_heading = models.CharField(max_length=100, blank=True)
    core_research_text = models.TextField(blank=True)
    certifications_heading = models.CharField(max_length=100, blank=True)
    certifications_text = models.TextField(blank=True)
    about_heading = models.CharField(max_length=100, blank=True)
    about_text = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'portfolio_profile'
        verbose_name_plural = 'Profile (CV_Portfolio)'


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=150, blank=True)
    quote = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} - {self.role}'

    class Meta:
        managed = False
        db_table = 'portfolio_testimonial'
        ordering = ['order']
        verbose_name_plural = 'Testimonials (CV_Portfolio)'


class Sample(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=100, blank=True)
    excerpt = models.TextField()
    body = models.TextField()
    published_at = models.DateField()
    is_published = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        managed = False
        db_table = 'portfolio_sample'
        ordering = ['order']
        verbose_name_plural = 'Showcase Samples (CV_Portfolio)'


class FurtherResearchSample(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=100, blank=True)
    excerpt = models.TextField()
    body = models.TextField()
    published_at = models.DateField()
    is_published = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        managed = False
        db_table = 'portfolio_furtherresearchsample'
        ordering = ['order']
        verbose_name_plural = 'Further Research Samples (CV_Portfolio)'
