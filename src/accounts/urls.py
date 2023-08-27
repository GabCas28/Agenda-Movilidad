from django.urls import path
from . import views
app_name = "accounts"

urlpatterns = [
    path("login", views.user_login, name="login"),
    path("logout", views.user_logout, name="logout"),
    path("signin", views.register, name="register"),
    path("staff_only", views.staff_only, name="staff_only"),
    path("password_updated", views.password_updated, name="password_updated"),
]
