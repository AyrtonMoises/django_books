from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('livros.urls')),
    path('', include('usuarios.urls')),
    path('', include('checkout.urls')),
    path('', include('paypal.standard.ipn.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
