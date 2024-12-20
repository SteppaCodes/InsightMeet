
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/schema", SpectacularAPIView.as_view(), name="schema"),
    path("api/", SpectacularSwaggerView.as_view(url_name="schema"), name="api"),

    path("api/auth/", include("apps.accounts.urls")),
    path("api/", include("apps.profiles.urls")),
    path("api/", include("apps.bookings.urls"))
]
