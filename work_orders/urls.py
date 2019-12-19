from django.urls import path, include
from . import views 


urlpatterns = [
    path('work_orders', views.work_orders, name='work_orders'),
]