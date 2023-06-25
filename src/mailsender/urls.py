from django.urls import path
from . import views

app_name = "sender"

urlpatterns = [
    # path('history/', views.history, name="list"),
    path('', views.form, name="form"),
    # path('<str:broadcast>', views.form, name="form"),
    # path('success/<str:broadcast>', views.success, name="success"),
]
