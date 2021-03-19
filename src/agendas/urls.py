from django.urls import path, include
from . import views

app_name="agendas"
urlpatterns = [
    path('', views.agenda_list, name="list"),
    path('categories/', views.categories, name="home"),
    path('categories/form/', views.category_form, name="category.form"),
    path('categories/form/<slug:category>', views.category_form, name="category.form"),
    path('form/', views.agenda_form, name="form"),
    path('form/<slug:slug>', views.agenda_form, name="form"),
    path('<slug:slug>', views.agenda_detail, name="detail"),
    path('<slug:slug>/import', include(("importer.urls", "home"), namespace='importer')), 
    path('<slug:slug>/contacts/', include("contacts.urls")),
    ]