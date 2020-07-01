from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("api_service.urls")),
    path("", include("find_dock.urls")),
]
