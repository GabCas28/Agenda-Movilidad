from django.urls import path, include
from . import views

app_name="templates"
urlpatterns = [
    path('', views.template_list, name="list"),
    path('categories/', views.categories, name="home"),
    path('categories/form/', views.category_form, name="category.form"),
    path('categories/form/<slug:category>', views.category_form, name="category.form"),
    path('form/', views.template_form, name="form"),
    path('form/<slug:slug>', views.template_form, name="form"),
    path('<slug:slug>', views.template_detail, name="detail")
    ]