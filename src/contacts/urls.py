from django.urls import path
from . import views

app_name = "contacts"

urlpatterns = [
    path('', views.contact_list, name="list"),
    path('<str:contact_id>', views.contact_detail, name="detail"),
    path('<str:contact_id>', views.contact_detail, name="form"),
    path('<str:contact_id>', views.contact_detail, name="modify"),
]
