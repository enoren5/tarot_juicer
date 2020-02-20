from django.urls import path
from . import views  # , include

urlpatterns = [
    path(
        'random_generator',
        views.RandomGenerator.as_view(),
        name='get_random_generator'
    ),
    path(
        'at_random/<int:generator_number>',
        views.at_random,
        name='at_random_with_number'
    ),
]
