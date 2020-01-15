from django.shortcuts import render
from django.http import HttpResponse
from .models import EssayArticle, CuratedSlashdot, CuratedWatchtower

''' def index(request):
    return HttpResponse('Hello, World?')'''


def article(request):
    articles = EssayArticle.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'essays/article.html', context)


def objections(request):
    return render(request, 'essays/objections.html')


def content_changelog(request):
    return render(request, 'essays/content_changelog.html')


def slashdot(request):
    articles = CuratedSlashdot.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'essays/slashdot.html', context)


def watchtower(request):
    articles = CuratedWatchtower.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'essays/watchtower.html', context)
