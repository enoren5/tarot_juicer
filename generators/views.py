from django.shortcuts import render


def at_random(request):
    return render(request, 'generators/at_random.html')
