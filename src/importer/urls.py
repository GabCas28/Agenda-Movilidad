from django.urls import path
from . import views

app_name = "importer"

urlpatterns = [
    path('', views.upload_file, name="main"),
    path('accept/<int:identifier>', views.accept_changes, name="accept"),
]
