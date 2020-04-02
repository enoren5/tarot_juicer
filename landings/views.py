from django.shortcuts import render
from .models import EssayList, AboutContent


def about(request):
    abouts = AboutContent.objects.all()
    context = {
        'abouts': abouts,
    }
    return render(request, 'landings/about.html', context)


def portal(request):
    return render(request, 'landings/portal.html')


def essay_list(request):
    essay_lists = EssayList.objects.all()
    context = {
        'essay_lists': essay_lists,
    }
    return render(request, 'landings/essay_list.html', context)
