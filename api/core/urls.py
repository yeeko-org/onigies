from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.shortcuts import redirect
from django.views.static import serve


admin.site.site_header = "ONIGIES"
admin.site.site_title = "ONIGIES"
admin.site.index_title = "ONIGIES"


urlpatterns = [
    path('', lambda request: redirect('admin/', permanent=False)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('api.urls')),
]


# Los archivos subidos se sirven bajo /files/ (renombrado desde /media/
# para no colisionar con el ONIGIES legado, que conserva /media/). Ruta
# explícita en vez de static() para que sirva con DEBUG=False; el prefijo
# se deriva de MEDIA_URL. Se omite cuando los archivos viven en S3.
if '://' not in settings.MEDIA_URL:
    _media_prefix = settings.MEDIA_URL.lstrip('/')
    urlpatterns += [
        re_path(rf'^{_media_prefix}(?P<path>.*)$', serve,
                {'document_root': settings.MEDIA_ROOT}),
    ]
urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)
# if settings.STATIC_URL:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
