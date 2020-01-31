from django.shortcuts import render
from django.http import JsonResponse
import json
from django.core.exceptions import ObjectDoesNotExist
from .models import Generator


def at_random(request, generator_number=None):
    try:
        if generator_number is not None:
            generator = Generator.objects.get(number=generator_number)
            next_card_number = Generator.objects.order_by('?').first().number
        else:
            generators = Generator.objects.order_by('?')
            generator = generators[0]
            next_card_number = generators[1].id

        cards = Generator.objects.all()


        context = {
            'generator': generator,
            'cards': cards,
            'next_card_number': next_card_number
        }

    except ObjectDoesNotExist:
        context = {
            'generator': None,
            'cards': None,
            'next_card_number': None
        }

    return render(request, 'generators/at_random.html', context)
