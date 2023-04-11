from django.urls import path,include
from . import views

urlpatterns = [
    # path('', views.index, name='index'), # former
    path('', views.Gateway.as_view(), name='index'), # former
    # path('login/',include('django.contrib.auth.urls')), # NEW with login_required 
    path('portal/', views.portal, name='portal'),
    path('logout/', views.EndSession.as_view(), name='logout'),
]

''' path('reentry', views.reentry, name='reentry'),
    path('register', views.register, name='register'),
    path('pending', views.pending, name='pending'),
    path('reset', views.reset, name='reset'), 
'''
    # path('dashboard', views.dashboard, name='dashboard'),
    # path('', views.index, name='index'),
    # path('login', views.login, name='login'),

