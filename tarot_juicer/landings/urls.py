from django.urls import path
from . import views  # , include

urlpatterns = [
    path('about', views.about, name='about'),
    path('essay_list', views.essay_list, name='essay_list'),
    path('how_to', views.how_to, name='how_to'),
]
