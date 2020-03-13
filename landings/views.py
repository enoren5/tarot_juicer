from django.shortcuts import render


def about(request):
    return render(request, 'landings/about.html')


def portal(request):
    return render(request, 'landings/portal.html')


def essay_list(request):
    return render(request, 'landings/essay_list.html')
