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


def curated_slashdot(request):
    return render(request, 'curated_slashdot/paper.html')


def curated_st_paul(request):
    return render(request, 'curated_st_paul/paper.html')
