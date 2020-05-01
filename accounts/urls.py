from django.urls import path
from . import views  # , include

urlpatterns = [
    path('', views.gateway, name='gateway'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    # path('dashboard', views.dashboard, name='dashboard'),
    # path('', views.index, name='index'),
    # path('login', views.login, name='login'),
]
