from django.urls import path, include
from . import views

app_name="templates"
urlpatterns = [
    path('', views.template_form, name="home"),
    path('categories/', views.categories, name="categories"),
    path('categories/form/', views.category_form, name="category.form"),
    path('categories/form/<slug:category>', views.category_form, name="category.form"),
    path('categories/delete/<str:category_id>', views.deleteCategory, name="category.delete"),
    path('form/', views.template_form, name="form"),
    path('form/<slug:slug>', views.template_form, name="form"),
    path('<slug:slug>', views.template_detail, name="detail"),
    path('delete/<str:template_id>', views.delete, name="delete")
    ]