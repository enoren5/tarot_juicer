from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.Gateway.as_view(), name='index'), # former
    path('portal/', views.portal, name='portal'),
    path('logout/', views.EndSession.as_view(), name='logout'),
]