from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.functions import datetime

class Agenda(models.Model):
    title =  models.CharField(max_length=199, default="")
    description= models.TextField(default="")
    slug= models.SlugField("")
    year = models.year = models.IntegerField(default=datetime.timezone.now().year, validators=[MinValueValidator(1970), MaxValueValidator(9999)])
    creation_date= models.DateField(auto_now_add=True)
    last_modified= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title 