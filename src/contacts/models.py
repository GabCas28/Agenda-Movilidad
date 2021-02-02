from django.db import models
from jsonfield import JSONField
from django.core.serializers.json import DjangoJSONEncoder
# Create your models here.
from agendas.models import Agenda
class Contact(models.Model):
    email = models.EmailField(default="")
    contact_info = JSONField(default={})
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    def __str__(self):
        return self.email     
    class Meta:
        unique_together = ("email", "agenda")