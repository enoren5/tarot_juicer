from django.shortcuts import render
from .models import Generator


def at_random(request):
    generator = Generator.objects.order_by('?').first()
    context = {
        'generator': generator,
    }

    return render(request, 'generators/at_random.html', context)
