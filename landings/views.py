from django.shortcuts import render


def about(request):
    return render(request, 'landings/about.html')


def portal(request):
    return render(request, 'landings/portal.html')


def site_map(request):
    return render(request, 'landings/site_map.html')
