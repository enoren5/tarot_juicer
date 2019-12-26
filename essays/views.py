from django.shortcuts import render
from django.http import HttpResponse


''' def index(request):
    return HttpResponse('Hello, World?')'''


def article(request):
    return render(request, 'essays/article.html')


def objections(request):
    return render(request, 'essays/objections.html')


def content_changelog(request):
    return render(request, 'essays/content_changelog.html')


def slashdot(request):
    return render(request, 'essays/slashdot.html')


def watchtower(request):
    return render(request, 'essays/watchtower.html')
