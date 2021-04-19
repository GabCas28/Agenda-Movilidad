from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from agendas.models import Agenda
import json
class Contact(models.Model):
    email = models.EmailField(default="", verbose_name="Email del contacto")
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE, verbose_name="Agenda asociada")
    contact_info =  models.JSONField(default=dict, blank=True, null=True, verbose_name="Información del contacto")


    def __str__(self):
        return str(self.agenda)+": "+self.email
    class Meta:
        unique_together = ("email", "agenda")

    @classmethod
    def create(cls, contact_info, agenda, email):
        contact = cls(contact_info=contact_info, agenda=agenda, email=email)
        return contact
        
    def getHeaders(self):
        contacts = Contact.objects.filter(agenda=self.agenda)
        headers = []
        for i in contacts:
            for key in i.contact_info:
                if key not in headers:
                    headers.append(key)

        return headers 