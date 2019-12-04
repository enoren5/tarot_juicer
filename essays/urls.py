from django.urls import path
from . import views  # , include

urlpatterns = [
    # path('', views.index, name='index'),
    path('article', views.article, name='article'),
    path('objections', views.objections, name='objections'),
    path('content_changelog', views.content_changelog, name='content_changelog'),
    path('curated_st_paul', views.curated_st_paul, name='curated_st_paul'),
    path('curated_slashdot', views.curated_slashdot, name='curated_slashdot'),
]
