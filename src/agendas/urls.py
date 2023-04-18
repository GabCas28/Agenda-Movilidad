from django.urls import path, include
from . import views

app_name="agendas"
urlpatterns = [
    path('agendas/', views.get_agendas, name="get_agendas"),
    path('', views.agenda_detail, name="home"),
    path('categories/', views.categories, name="categoreis"),
    path('categories/form/', views.category_form, name="category.form"),
    path('categories/form/<slug:category>', views.category_form, name="category.form"),
    path('categories/delete/<str:category_id>', views.deleteCategory, name="category.delete"),
    path('form/', views.agenda_form, name="form"),
    path('form/<slug:slug>', views.agenda_form, name="form"),
    path('<slug:slug>', views.agenda_detail, name="detail"),
    path('<slug:slug>/import', include(("importer.urls", "home"), namespace='importer')), 
    path('<slug:slug>/contacts/', include("contacts.urls")),
    path('delete/<str:agenda_id>', views.delete, name="delete"),
    ]