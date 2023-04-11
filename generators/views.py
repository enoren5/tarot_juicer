from django.shortcuts import render
from django.http import HttpResponseRedirect
import json
from django.core.exceptions import ObjectDoesNotExist
from .models import Generator
from django.views.generic import View
from django.urls import reverse
from accounts.models import AuthToggle
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class RandomGenerator(LoginRequiredMixin,View):

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


@login_required
def getPrevNext(array, element):
    result = array.index(element)
    return  [array[result - 1], array[(result + 1) % len(array)]]


@login_required
def tarot_key(request, generator_number):
    # try:
    #     generator_obj = Generator.objects.get(is_published=True)
    # except Generator.DoesNotExist:
    #     raise Http404("Generator Doesn't exists!")
    try:
        generator = Generator.objects.filter(
            number=generator_number).first()
        print("\n Generator :", generator)
        next_card_number = Generator.objects.order_by('?').first().number

        generator_array = []

        for value in Generator.objects.order_by('number'):
            generator_array.append(value.number)

        prev_generator, next_generator = getPrevNext(generator_array, generator_number)
        
        cards = Generator.objects.order_by('number')
        context = {
            # 'generator_obj': generator_obj,
            'generator': generator,
            'cards': cards,
            'next_card_number': next_card_number,
            "protection": AuthToggle.objects.first(),
            'prev_generator': prev_generator,
            'next_generator': next_generator,
            "email": AuthToggle.objects.first(),
        }

    except ObjectDoesNotExist:
        context = {
            'generator': None,
            'cards': None,
            'next_card_number': None,
            "protection": AuthToggle.objects.first(),
            'prev_generator': None,
            'next_generator': None,
            "email": AuthToggle.objects.first(),
        }

    return render(request, 'generators/tarot_key.html', context)
