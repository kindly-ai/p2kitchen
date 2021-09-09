from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

from p2coffee import urls as p2coffee_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(p2coffee_urls)),
    # FIXME: Hack in static file serving
    re_path(r"^static/(?P<path>.*)$", serve, kwargs={"document_root": settings.STATIC_ROOT}),
]
