from django.shortcuts import render
from django.http import HttpResponseRedirect
import json
from django.core.exceptions import ObjectDoesNotExist
from .models import Generator
from django.views.generic import View
from django.urls import reverse


class RandomGenerator(View):

    def get(self, request, *args, **kwargs):
        """
        Get random generator and redirects to tarot_key template using
        number randomly 
        """
        try:
            generator = Generator.objects.values('number').order_by('?')[0]
        except Exception as e:
            generator = {}

        return HttpResponseRedirect(
            reverse(
                'tarot_key_with_number',
                kwargs={'generator_number': generator['number']}
            )
        )


def tarot_key(request, generator_number):
    try:
        generator = Generator.objects.filter(
            number=generator_number).first()
        next_card_number = Generator.objects.order_by('?').first().number

        cards = Generator.objects.order_by('number')
        context = {
            'generator': generator,
            'cards': cards,
            'next_card_number': next_card_number
        }

    except ObjectDoesNotExist:
        context = {
            'generator': None,
            'cards': null,
            'next_card_number': None
        }

    return render(request, 'generators/tarot_key.html', context)
