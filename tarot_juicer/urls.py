from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', include('essays.urls')),
    path('', include('generators.urls')),
    path('', include('landings.urls')),
    # path('', include('accounts.urls')),
    # path('', include('generators.urls')),
    # path('', include('landings.urls')),
    path("", include("gateway_defender.urls")),
    path("cookies/", include("cookie_consent.urls")),
    path(settings.ADMIN_PATH, admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Tarot Juicer'
admin.site.site_title = 'Tarot Juicer'

handler404 = 'tarot_juicer.views.handler404'
handler500 = 'tarot_juicer.views.handler500'