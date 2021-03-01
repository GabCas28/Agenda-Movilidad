from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.functions import datetime

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class MailTemplate(models.Model):
    title = models.CharField(max_length=100, default="", blank=True)
    slug = models.SlugField(default="", unique=True)
    category = models.ForeignKey(
        Category, blank=True, null=True, on_delete=models.CASCADE)
    description = models.TextField(max_length=199, default="", blank=True)
    subject = models.CharField(max_length=100, default="", blank=True)
    content = models.TextField(blank=True, default="")
    year = models.year = models.IntegerField(default=datetime.timezone.now(
    ).year, validators=[MinValueValidator(1970), MaxValueValidator(9999)])
    creation_date = models.DateField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title     