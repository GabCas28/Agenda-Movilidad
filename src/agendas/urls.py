from django.urls import path, include
from . import views

app_name="agendas"
urlpatterns = [
    path('', views.agenda_list, name="home"),
    path('form/', views.agenda_form, name="form"),
    path('form/<str:agenda_id>', views.agenda_form, name="form"),
    path('<slug:slug>', views.agenda_detail, name="detail"),
    path('<slug:slug>/import', include(("importer.urls", "home"), namespace='importer'))
    ]