from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from agendas.models import Agenda

class ContactManager(models.Manager):
    def create_contact(self, contact_info):
        contact = self.create(contact_info=contact_info)
        # do something with the book
        return contact


class Contact(models.Model):
    email = models.EmailField(default="")
    contact_info =  models.JSONField(default=dict, blank=True, null=True)
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    def __str__(self):
        return self.email     
    class Meta:
        unique_together = ("email", "agenda")

    @classmethod
    def create(cls, contact_info, agenda, email):
        contact = cls(contact_info=contact_info, agenda=agenda, email=email)
        return contact