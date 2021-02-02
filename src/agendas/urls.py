from django.urls import path
from . import views

app_name="agendas"
urlpatterns = [
    path('', views.agenda_list, name="home"),
    path('<slug:slug>', views.agenda_detail, name="detail"),
]
