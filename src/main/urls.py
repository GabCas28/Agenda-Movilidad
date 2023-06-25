from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("import/", include("importer.urls")),
    path("models/", include("mailtemplates.urls")),
    path("sender/", include("mailsender.urls")),
    path("summernote/", include("django_summernote.urls")),
    path("agendas/", include("agendas.urls")),
    path("", views.home),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
