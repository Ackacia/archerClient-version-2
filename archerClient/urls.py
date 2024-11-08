from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from appServicesEvals.views import dashboard

admin.site.site_header = "L'Archer QR Code Admin"
admin.site.site_title = "L'Archer QR Code"
admin.site.index_title = "Bienvenue dans l'administration L'Archer QRCode"
admin.site.site_header = "L'Archer QR Code Admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name="dashboard"),
    path('gestion-evenement/', include('appGestEvenements.urls')),
    path('service-evaluation/', include('appServicesEvals.urls')),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, )

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)