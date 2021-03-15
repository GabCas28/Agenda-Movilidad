from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from agendas.models import Agenda
class Contact(models.Model):
    email = models.EmailField(default="")
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    contact_info =  models.JSONField(default=dict, blank=True, null=True)


    def __str__(self):
        return self.email +"-"+str(self.agenda)
    class Meta:
        unique_together = ("email", "agenda")

    @classmethod
    def create(cls, contact_info, agenda, email):
        contact = cls(contact_info=contact_info, agenda=agenda, email=email)
        return contact