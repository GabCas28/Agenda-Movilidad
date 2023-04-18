from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from agendas.models import Agenda
import json


class Contact(models.Model):
    email = models.EmailField(
        default="", verbose_name="Email del contacto"
    )  # Email of the contact
    agenda = models.ForeignKey(
        Agenda, on_delete=models.CASCADE, verbose_name="Agenda asociada"
    )  # Associated agenda
    contact_info = models.JSONField(
        default=dict, blank=True, null=True, verbose_name="Información del contacto"
    )  # JSON field to store contact information

    def __str__(self):
        return (
            str(self.agenda) + ": " + self.email
        )  # String representation of the contact object

    class Meta:
        unique_together = (
            "email",
            "agenda",
        )  # Contact objects should be unique based on email and agenda

    @classmethod
    def create(cls, contact_info, agenda, email):
        """
        A class method to create a new Contact object with the provided information.

        Parameters:
        - contact_info: A dictionary containing the contact information.
        - agenda: An Agenda object representing the associated agenda.
        - email: The email address of the contact.

        Returns:
        A new Contact object with the provided information.
        """
        contact = cls(contact_info=contact_info, agenda=agenda, email=email)
        return contact

    def getHeaders(self):
        """
        A method to get a list of all unique keys in the contact_info JSON field across all Contact objects
        associated with the same agenda as the current Contact object.

        Returns:
        A list of all unique keys in the contact_info JSON field across all Contact objects associated with
        the same agenda as the current Contact object.
        """
        headers = set()
        for contact in Contact.objects.filter(agenda=self.agenda):
            headers |= set(contact.contact_info.keys())
        return list(headers)
