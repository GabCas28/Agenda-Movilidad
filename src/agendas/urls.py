from django.urls import path
from . import views

urlpatterns = [
    path('', views.agenda_list, name="home"),
    path('<slug:slug>', views.agenda_detail, name="agenda_detail"),
]
