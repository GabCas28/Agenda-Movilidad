from django.urls import path
from . import views

app_name = "sender"

urlpatterns = [
    path('', views.history, name="list"),
    path('form', views.form, name="form"),
    path('form/<str:broadcast>', views.form, name="form"),
    path('success/<str:broadcast>', views.success, name="success"),
]
