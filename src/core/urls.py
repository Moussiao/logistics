from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from src.core.api import api

urlpatterns = [
    path("api/", api.urls),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        # URLs specific only to django-debug-toolbar:
        path("__debug__/", include(debug_toolbar.urls)),
    ]
