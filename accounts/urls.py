from django.urls import path
from . import views  # , include

urlpatterns = [
    path('', views.index, name='index'),
    path('portal', views.portal, name='portal'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('pending', views.pending, name='pending'),
    path('logout', views.logout, name='logout'),
    path('reset', views.reset, name='reset'),
    # path('dashboard', views.dashboard, name='dashboard'),
    # path('', views.index, name='index'),
    # path('login', views.login, name='login'),
]
