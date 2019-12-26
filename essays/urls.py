from django.urls import path
from . import views  # , include

urlpatterns = [
    # path('', views.index, name='index'),
    path('article', views.article, name='article'),
    path('objections', views.objections, name='objections'),
    path('content_changelog', views.content_changelog, name='content_changelog'),
    path('watchtower', views.watchtower, name='watchtower'),
    path('slashdot', views.slashdot, name='slashdot'),
]
