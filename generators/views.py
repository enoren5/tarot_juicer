from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from .models import Generator


def at_random(request):
    try:
        generator = Generator.objects.order_by('?').first()
        context = {
            'generator': generator,
        }
    except ObjectDoesNotExist:
        context = {
            'generator': None
        }

    return render(request, 'generators/at_random.html', context)
