from django.shortcuts import render
from django.http import HttpResponse
from .models import EssayArticle, CuratedSlashdot, CuratedWatchtower, ContentChanges, ObjectionsArticle, BibliographyArticle, ContentDump
from generators.models import Generator

''' def index(request):
    return HttpResponse('Hello, World?')'''


def slashdot(request):
    slashdot_obj = CuratedSlashdot.objects.order_by('?').first()
    generators = Generator.objects.filter(slashdot_position__isnull=False).order_by('slashdot_position')

    context = {
        'slashdot_obj': slashdot_obj,
        'generators': generators,
    }
    return render(request, 'essays/slashdot.html', context)


def watchtower(request):
    articles = CuratedWatchtower.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'essays/watchtower.html', context)


def article(request, web_address):
    articles = EssayArticle.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'essays/article.html', context)


def objections(request):
    articles = ObjectionsArticle.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'essays/objections.html', context)


def content_changelog(request):
    changes = ContentChanges.objects.all()
    context = {
        'changes': changes,
    }
    return render(request, 'essays/content_changelog.html', context)


def bibliography(request):
    articles = BibliographyArticle.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'essays/bibliography.html', context)


def all_content_dump(request):
    context = {
        'generators': Generator.objects.all().order_by('number'),
        'essay_articles': EssayArticle.objects.all(),
        'slashdots': CuratedSlashdot.objects.all(),
        'watchowers': CuratedWatchtower.objects.all(),
        'content_changes': ContentChanges.objects.all(),
        'objections_articles': ObjectionsArticle.objects.all(),
        'biblio_articles': BibliographyArticle.objects.all()
    }
    return render(request, 'essays/all_content_dump.html', context)
