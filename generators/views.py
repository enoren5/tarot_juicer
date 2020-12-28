from django.shortcuts import render
from django.http import HttpResponseRedirect
import json
from django.core.exceptions import ObjectDoesNotExist
from .models import Generator
from django.views.generic import View
from django.urls import reverse
from accounts.models import get_random_visitor_name

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
        if request.session.has_key('username'):
            user_name = request.session['username']
        else:
            user_name = get_random_visitor_name()

        return HttpResponseRedirect(
            reverse(
                'tarot_key_with_number',
                kwargs={'generator_number': generator['number'], 'user_name': user_name}
            )
        )


def tarot_key(request, generator_number, user_name):
    try:
        generator = Generator.objects.filter(
            number=generator_number).first()
        next_card_number = Generator.objects.order_by('?').first().number

        cards = Generator.objects.order_by('number')
        context = {
            'generator': generator,
            'cards': cards,
            'next_card_number': next_card_number,
            'user_name': user_name
        }

    except ObjectDoesNotExist:
        context = {
            'generator': None,
            'cards': None,
            'next_card_number': None,
            'user_name': user_name
        }

    return render(request, 'generators/tarot_key.html', context)
