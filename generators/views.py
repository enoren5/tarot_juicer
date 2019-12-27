from django.shortcuts import render
from django.http import JsonResponse
import json
from django.core.exceptions import ObjectDoesNotExist
from .models import Generator


def at_random(request, generator_id=None):
    try:
        if generator_id is not None:
            generator = Generator.objects.get(id=generator_id)
            next_card_id = Generator.objects.order_by('?').first().id
        else:
            generators = Generator.objects.order_by('?')
            generator = generators[0]
            next_card_id = generators[1].id

        context = {
            'generator': generator,
            'next_card_id': next_card_id
        }

    except ObjectDoesNotExist:
        context = {
            'generator': None,
            'next_card_id': None
        }

    return render(request, 'generators/at_random.html', context)
