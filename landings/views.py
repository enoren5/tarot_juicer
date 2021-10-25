from django.shortcuts import render
from .models import EssayList, AboutContent, HowTo
from accounts.models import AuthToggle

def about(request):
    abouts = AboutContent.objects.all()

    context = {
        'abouts': abouts,
        "protection": AuthToggle.objects.first()
    }

    return render(request, 'landings/about.html', context)


def portal(request):
    context = {
        "protection": AuthToggle.objects.first()
    }
    return render(request, 'landings/portal.html', context)


def essay_list(request):
    essay_lists = EssayList.objects.all()
    context = {
        'essay_lists': essay_lists,
        "protection": AuthToggle.objects.first()
    }
    return render(request, 'landings/essay_list.html', context)


def how_to(request):
    how_tos = HowTo.objects.all()
    context = {
        'how_tos': how_tos,
        "protection": AuthToggle.objects.first()
    }
    return render(request, 'landings/how_to.html', context)


def reentry(request):
    context = {
        "protection": AuthToggle.objects.first()
    }
    return render(request, 'landings/reentry.html', context)