from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import EssayArticle, CuratedSlashdot, CuratedWatchtower, ContentChanges, ObjectionsArticle, BibliographyArticle
from landings.models import EssayList, AboutContent, HowTo
from generators.models import Generator
from accounts.models import AuthToggle

''' def index(request):
    return HttpResponse('Hello, World?')'''


def slashdot(request):
    print("SlashDot")
    try:
        print("SlashDot")
        slashdot_obj = CuratedSlashdot.objects.get(is_published=True)
        print("SlashDot", slashdot_obj)
    except CuratedSlashdot.DoesNotExist:
        raise Http404("Slashdot doesn't exists!")
    generators = Generator.objects.filter(
        slashdot_position__isnull=False).order_by('slashdot_position')
    biblio_objs =  BibliographyArticle.objects.all()
    context = {
        'slashdot_obj': slashdot_obj,
        'generators': generators,
        "protection": AuthToggle.objects.first(),
        'biblio_objs': biblio_objs,
    }
    return render(request, 'essays/slashdot.html', context)


def watchtower(request):
    try:
        watchtower_obj = CuratedWatchtower.objects.get(is_published=True)
        print("Watchtower", watchtower_obj)
    except CuratedWatchtower.DoesNotExist:
        raise Http404("Watchtower Doesn't exists!")
    generators = Generator.objects.filter(
        watchtower_position__isnull=False).order_by('watchtower_position')
    biblio_objs =  BibliographyArticle.objects.all()
    context = {
        'watchtower_obj': watchtower_obj,
        'generators': generators,
        "protection": AuthToggle.objects.first(),
        'biblio_objs': biblio_objs,        
    }
    return render(request, 'essays/watchtower.html', context)


def article(request, web_address):
    try:
        article = EssayArticle.objects.get(
            web_address_slug=web_address, is_published=True)
        biblio_objs =  BibliographyArticle.objects.all()

    except EssayArticle.DoesNotExist:
        raise Http404('Article does not exist!')
    context = {
        'article': article,
        "protection": AuthToggle.objects.first(),
        'biblio_objs': biblio_objs,
    }
    return render(request, 'essays/article.html', context)


def objections(request):
    articles = ObjectionsArticle.objects.all()
    context = {
        'articles': articles,
        "protection": AuthToggle.objects.first()
    }
    return render(request, 'essays/objections.html', context)


def content_changelog(request):
    changes = ContentChanges.objects.all()
    context = {
        'changes': changes,
        "protection": AuthToggle.objects.first()
    }
    return render(request, 'essays/content_changelog.html', context)


def bibliography(request):
    articles = BibliographyArticle.objects.all()
    context = {
        'articles': articles,
        "protection": AuthToggle.objects.first()
    }
    return render(request, 'essays/bibliography.html', context)


def all_content_dump(request):
    context = {
        'generators': Generator.objects.all().order_by('number'),
        'essay_articles': EssayArticle.objects.all(),
        'slashdots': CuratedSlashdot.objects.all(),
        'watchtowers': CuratedWatchtower.objects.all(),
        'content_changes': ContentChanges.objects.all(),
        'objections_articles': ObjectionsArticle.objects.all(),
        'biblio_articles': BibliographyArticle.objects.all(),
        "protection": AuthToggle.objects.first(),
        'essay_lists': EssayList.objects.all(), 
        'abouts': AboutContent.objects.all(),
        'how_tos': HowTo.objects.all(),
    }
    return render(request, 'essays/all_content_dump.html', context)
