from django.shortcuts import render
from .models import EssayList, AboutContent, HowTo
from accounts.models import AuthToggle
from django.contrib.auth.decorators import login_required
from django.http import Http404 # HttpResponse
from accounts.custom_decorator import protected_redirect


@protected_redirect
def about(request):
    try:
        about_content_obj = AboutContent.objects.get(is_published=True)
    except AboutContent.DoesNotExist:
        raise Http404('About Content does not exist!')
    abouts = AboutContent.objects.all()

    context = {
        'about_content_obj': about_content_obj,
        'abouts': abouts,
        "protection": AuthToggle.objects.first(),
        "email": AuthToggle.objects.first(),
    }

    return render(request, 'landings/about.html', context)


@protected_redirect
def portal(request):
    context = {
        "protection": AuthToggle.objects.first(),
        "email": AuthToggle.objects.first(),
    }
    return render(request, 'landings/portal.html', context)


@protected_redirect
def essay_list(request):
    try:
        essay_list_obj = EssayList.objects.get(is_published=True)
    except EssayList.DoesNotExist:
        raise Http404('Essay List does not exist!')
    essay_lists = EssayList.objects.all()
    context = {
        'essay_list_obj': essay_list_obj,
        'essay_lists': essay_lists,
        "protection": AuthToggle.objects.first(),
        "email": AuthToggle.objects.first(),
    }
    return render(request, 'landings/essay_list.html', context)


@protected_redirect
def how_to(request):
    try:
        how_to_obj = HowTo.objects.get(is_published=True)
    except HowTo.DoesNotExist:
        raise Http404('HowTo does not exist!')
    how_tos = HowTo.objects.all()
    context = {
        'how_to_obj': how_to_obj,
        'how_tos': how_tos,
        "protection": AuthToggle.objects.first(),
        "email": AuthToggle.objects.first(),
    }
    return render(request, 'landings/how_to.html', context)


@protected_redirect
def reentry(request):
    context = {
        "protection": AuthToggle.objects.first()
    }
    return render(request, 'landings/reentry.html', context)
