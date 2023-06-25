from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.functions import datetime


class Category(models.Model):
    title = models.CharField(max_length=200, verbose_name="Nombre")
    slug = models.SlugField(verbose_name="URL", unique=True)

    def __str__(self):
        return self.title


class Agenda(models.Model):
    title = models.CharField(max_length=199, default="", verbose_name="Título")
    slug = models.SlugField(default="", unique=True, verbose_name="URL amigable")
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Categoría",
    )
    year = models.year = models.IntegerField(
        default=datetime.timezone.now().year,
        validators=[MinValueValidator(1970), MaxValueValidator(9999)],
        verbose_name="Año",
    )
    creation_date = models.DateField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.year) + "-" + str(self.category) + "-" + self.title
