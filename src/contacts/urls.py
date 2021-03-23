from django.urls import path
from . import views

app_name = "contacts"

urlpatterns = [
    path('', views.contact_list, name="list"),
    path('form', views.contact_form, name="form"),
    path('form/<str:contact_id>', views.contact_form, name="form"),
    path('<str:contact_id>', views.contact_detail, name="detail"),
    path('delete/<str:contact_id>', views.delete, name="delete")
]
