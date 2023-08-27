from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("import/", include("importer.urls")),
    path("models/", include("mailtemplates.urls")),
    path("sender/", include("mailsender.urls")),
    path("summernote/", include("django_summernote.urls")),
    path("agendas/", include("agendas.urls")),
    path("", views.home),
    # Forgot password URLS
    path(
        "reset-password/", auth_views.PasswordResetView.as_view(), name="password_reset"
    ),
    path(
        "reset-password/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset-password/confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset-password/complete/",
        views.password_updated,
        name="password_reset_complete",
    ),
    # Change passowrd URLs
    path(
        "change-password/",
        auth_views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path("change-password/done/", views.password_updated, name="password_change_done"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
