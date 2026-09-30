"""
Mirrors hypno_mixer's contents.* models, which live in the same Postgres
instance as this project. managed=False means this app's migrations never
touch the tables' schema - hypno_mixer remains the sole owner of that.
excluded_users (M2M to hypno_mixer's own auth.User table) isn't mirrored
since it's not needed for read-only display here.

Used exclusively by essays.views.all_content_dump - these models are not
registered in admin and have no other views pointed at them.
"""

from django.db import models


class Preamble(models.Model):
    title = models.CharField(max_length=300, blank=True)
    is_published = models.BooleanField(default=True)
    author = models.CharField(max_length=30, blank=True)
    slug = models.SlugField(blank=True)
    body = models.TextField(max_length=300000, blank=True)
    publication_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        managed = False
        db_table = 'contents_preamble'
        verbose_name_plural = 'Preambles (hypno_mixer)'


class Induction(models.Model):
    title = models.CharField(max_length=300, blank=True)
    is_published = models.BooleanField(default=True)
    essential = models.BooleanField(default=False, blank=True)
    author = models.CharField(max_length=30, blank=True)
    slug = models.SlugField(blank=True)
    body = models.TextField(max_length=300000, blank=True)
    publication_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        managed = False
        db_table = 'contents_induction'
        verbose_name_plural = 'Inductions (hypno_mixer)'


class ScriptSuggestion(models.Model):
    title = models.CharField(max_length=300, blank=True)
    is_published = models.BooleanField(default=True)
    essential = models.BooleanField(default=False, blank=True)
    author = models.CharField(max_length=300, blank=True)
    slug = models.SlugField(blank=True)
    body = models.TextField(max_length=300000, blank=True)
    publication_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        managed = False
        db_table = 'contents_scriptsuggestion'
        verbose_name_plural = 'Scripting - Custom (hypno_mixer)'


class Research(models.Model):
    title = models.CharField(max_length=300, blank=True)
    is_published = models.BooleanField(default=True)
    essential = models.BooleanField(default=False, blank=True)
    author = models.CharField(max_length=300, blank=True)
    slug = models.SlugField(blank=True)
    body = models.TextField(max_length=300000, blank=True)
    publication_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        managed = False
        db_table = 'contents_research'
        verbose_name_plural = 'Research (hypno_mixer)'


class StockScript(models.Model):
    title = models.CharField(max_length=300, blank=True)
    is_published = models.BooleanField(default=True)
    essential = models.BooleanField(default=False, blank=True)
    author = models.CharField(max_length=300, blank=True)
    slug = models.SlugField(blank=True)
    body = models.TextField(max_length=300000, blank=True)
    publication_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        managed = False
        db_table = 'contents_stockscript'
        verbose_name_plural = 'Scripting - Stock (hypno_mixer)'


class NYTimes(models.Model):
    title = models.CharField(max_length=300, blank=True)
    is_published = models.BooleanField(default=True)
    essential = models.BooleanField(default=False, blank=True)
    author = models.CharField(max_length=300, blank=True)
    slug = models.SlugField(blank=True)
    body = models.TextField(max_length=300000, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        managed = False
        db_table = 'contents_nytimes'
        verbose_name_plural = 'NY Times (hypno_mixer)'


class TorStar(models.Model):
    title = models.CharField(max_length=300, blank=True)
    is_published = models.BooleanField(default=True)
    essential = models.BooleanField(default=False, blank=True)
    author = models.CharField(max_length=300, blank=True)
    slug = models.SlugField(blank=True)
    body = models.TextField(max_length=300000, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        managed = False
        db_table = 'contents_torstar'
        verbose_name_plural = 'Toronto Star (hypno_mixer)'


class WSJournal(models.Model):
    title = models.CharField(max_length=300, blank=True)
    is_published = models.BooleanField(default=True)
    essential = models.BooleanField(default=False, blank=True)
    author = models.CharField(max_length=300, blank=True)
    slug = models.SlugField(blank=True)
    body = models.TextField(max_length=300000, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        managed = False
        db_table = 'contents_wsjournal'
        verbose_name_plural = 'WSJ (hypno_mixer)'


class AssortedPeriodicals(models.Model):
    media_type = models.CharField(max_length=300, blank=True)
    author_last_name = models.CharField(max_length=300, blank=True)
    publication_year = models.CharField(max_length=300, blank=True)
    address = models.CharField(max_length=300, blank=True)
    title = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return f'{self.author_last_name} {self.title}'

    class Meta:
        managed = False
        db_table = 'contents_assortedperiodicals'
        verbose_name_plural = 'Assorted Periodicals (hypno_mixer)'


class AssortedLiterature(models.Model):
    media_type = models.CharField(max_length=300, blank=True)
    author_last_name = models.CharField(max_length=300, blank=True)
    publication_year = models.CharField(max_length=300, blank=True)
    address = models.CharField(max_length=300, blank=True)
    title = models.CharField(max_length=300, blank=True)
    publication_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.author_last_name} {self.title}'

    class Meta:
        managed = False
        db_table = 'contents_assortedliterature'
        verbose_name_plural = 'Assorted Literature (hypno_mixer)'


class Binaurals(models.Model):
    author_last_name = models.CharField(max_length=300, blank=True)
    publication_year = models.CharField(max_length=300, blank=True)
    address = models.CharField(max_length=300, blank=True)
    title = models.CharField(max_length=300, blank=True)
    publication_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.author_last_name} {self.title}'

    class Meta:
        managed = False
        db_table = 'contents_binaurals'
        verbose_name_plural = 'Binaurals (hypno_mixer)'
