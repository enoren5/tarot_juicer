from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', include('essays.urls')),
    path('', include('generators.urls')),
    path('', include('landings.urls')),
    path('', include('work_orders.urls')),
    path('', include('accounts.urls')),
    # path('', include('generators.urls')),
    # path('', include('landings.urls')),
    path(settings.ADMIN_PATH, admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Tarot Juicer'
admin.site.site_title = 'Tarot Juicer'

handler404 = 'tarot_juicer.views.handler404'
handler500 = 'tarot_juicer.views.handler500'

"""tarot_juicer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
