from django.shortcuts import render
from .models import EssayList, AboutContent
from accounts.models import get_random_visitor_name

def about(request, user_name):
    abouts = AboutContent.objects.all()

    if request.session.has_key('username'):
        user_name = request.session['username']
    else:
        user_name = get_random_visitor_name()
    context = {
        'abouts': abouts,
        'user_name': user_name
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
