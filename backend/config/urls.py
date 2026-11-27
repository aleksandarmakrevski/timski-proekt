from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts_views import RegisterView, MeView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/register/", RegisterView.as_view(), name="register"),
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/me/", MeView.as_view(), name="me"),
    path("api/hotel/", include("hotels.urls")),
    path("api/rooms/", include("rooms.urls")),
    path("api/reservations/", include("reservations.urls")),
    path("api/contact/", include("contact.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
