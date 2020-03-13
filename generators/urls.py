from django.urls import path
from . import views  # , include

urlpatterns = [
    path(
        'tarot_key_generator',
        views.RandomGenerator.as_view(),
        name='get_tarot_key_generator'
    ),
    path(
        'tarot_key/<int:generator_number>',
        views.tarot_key,
        name='tarot_key_with_number'
    ),
]
