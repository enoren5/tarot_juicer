from django.shortcuts import render
from .models import Generator


def at_random(request):

    generators = Generator.objects.all()

    context = {
        'generators': generators,
    }

    return render(request, 'generators/at_random.html', context)
