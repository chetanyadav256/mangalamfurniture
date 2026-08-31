from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path

from core.views import ManglamAdminLoginView, admin_forgot_password, admin_reset_password, admin_verify_pin


def profile_redirect(request):
    return redirect("admin:index")


urlpatterns = [
    path("admin/login/", ManglamAdminLoginView.as_view(), name="admin_login"),
    path("admin/forgot-password/", admin_forgot_password, name="admin_forgot_password"),
    path("admin/verify-pin/", admin_verify_pin, name="admin_verify_pin"),
    path("admin/reset-password/", admin_reset_password, name="admin_reset_password"),
    path("accounts/profile/", profile_redirect, name="profile_redirect"),
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("shop/", include("catalog.urls")),
    path("", include("shop_info.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)