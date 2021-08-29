from django.urls import include, path
from django.contrib import admin

from p2coffee import urls as p2coffee_urls

urlpatterns = [path("admin/", admin.site.urls), path("", include(p2coffee_urls))]
