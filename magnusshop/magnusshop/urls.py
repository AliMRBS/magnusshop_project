from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('magnusplus/', include('magnusplus.urls', namespace='magnusplus')), 
    path('cart/', include('cart.urls')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('finance/', include('finance.urls', namespace='finance')),
    path('account/', include('account.urls', namespace='account')),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)