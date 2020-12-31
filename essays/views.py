from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import EssayArticle, CuratedSlashdot, CuratedWatchtower, ContentChanges, ObjectionsArticle, BibliographyArticle
from generators.models import Generator
from accounts.models import get_random_visitor_name

''' def index(request):
    return HttpResponse('Hello, World?')'''


def slashdot(request, user_name):
    slashdot_obj = CuratedSlashdot.objects.order_by('?').first()
    generators = Generator.objects.filter(
        slashdot_position__isnull=False).order_by('slashdot_position')
    if request.session.has_key('username'):
        user_name = request.session['username']
    else:
        user_name = get_random_visitor_name()
    context = {
        'slashdot_obj': slashdot_obj,
        'generators': generators,
        'user_name': user_name
    }
    return render(request, 'essays/slashdot.html', context)


def watchtower(request, user_name):
    watchtower_obj = CuratedWatchtower.objects.order_by('?').first()
    generators = Generator.objects.filter(
        watchtower_position__isnull=False).order_by('watchtower_position')
    if request.session.has_key('username'):
        user_name = request.session['username']
    else:
        user_name = get_random_visitor_name()
    context = {
        'watchtower_obj': watchtower_obj,
        'generators': generators,
        'user_name': user_name
    }
    return render(request, 'essays/watchtower.html', context)


def article(request, web_address):
    try:
        article = EssayArticle.objects.get(
            web_address_slug=web_address, is_published=True)
    except EssayArticle.DoesNotExist:
        raise Http404('Article does not exist!')
    context = {
        'article': article,
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
