from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("eprocurement/", include("dashboard.urls")),
    path("eprocurement/", include("authentication.urls")),
    path("eprocurement/", include("base.urls")),
]
