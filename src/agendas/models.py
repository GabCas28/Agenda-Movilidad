from django.db import models

# Create your models here.
class Agenda(models.Model):
    title=  models.CharField(max_length=199)
    description= models.TextField()
    slug= models.SlugField()
    creation_date= models.DateField(auto_now_add=True)
    last_modified= models.DateTimeField()

    def __str__(self):
        return self.title 