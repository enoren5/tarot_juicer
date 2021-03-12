from django.urls import path
from . import views  # , include

urlpatterns = [
    # path('', views.index, name='index'),
    path('article/watchtower/', views.watchtower, name='watchtower'),
    path('article/slashdot/', views.slashdot, name='slashdot'),
    path('article/<str:web_address>/', views.article, name='article'),
    path('article/objections/', views.objections, name='objections'),
    path('article/content_changelog/',
         views.content_changelog, name='content_changelog'),
    path('article/bibliography/', views.bibliography, name='bibliography'),
    path('article/all_content_dump/',
         views.all_content_dump, name='all_content_dump')

]