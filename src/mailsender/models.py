from django.db import models
from contacts.models import Contact
from django.template import Context, Template
import logging

logger = logging.getLogger("logging.StreamHandler")


class MassMail(models.Model):
    subject = models.CharField(
        max_length=100, default="", blank=True, verbose_name="Asunto"
    )
    content = models.TextField(blank=True, default="", verbose_name="Cuerpo")
    recipients = models.ManyToManyField(Contact, verbose_name="Destinatarios")
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.creation_date) + "_" + str(self.subject)

    def create_emails(self):
        template = Template(self.content)
        subject = Template(self.subject)
        contacts = self.recipients.all()
        mails = []

        for contact in contacts:
            mail_subject = subject.render(Context(contact.contact_info))
            mail_content = template.render(Context(contact.contact_info))
            mails.append(([contact.email, mail_subject, mail_content]))

        return mails
