from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.functions import datetime
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class Category(models.Model):
    title = models.CharField(max_length=200, verbose_name="Nombre")
    slug = models.SlugField(verbose_name="Slug de la categoría (URL amigable)")
    def __str__(self):
        return self.title

class MailTemplate(models.Model):
    year = models.year = models.IntegerField(default=datetime.timezone.now(
    ).year, validators=[MinValueValidator(1970), MaxValueValidator(9999)], verbose_name="Año")
    category = models.ForeignKey(
        Category, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Categoría")
    title = models.CharField(max_length=100, default="", blank=True, verbose_name="Título")
    slug = models.SlugField(default="", unique=True, verbose_name="URL amigable")
    subject = models.CharField(max_length=100, default="", blank=True, verbose_name="Asunto")
    content = models.TextField(blank=True, default="", verbose_name="Cuerpo del mensaje")
    
    creation_date = models.DateField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title     