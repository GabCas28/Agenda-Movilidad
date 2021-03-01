from django.db import models
from mailtemplates.models import MailTemplate
from agendas.models import Agenda
from contacts.models import Contact
from django.core.mail import send_mass_mail, get_connection
from django.template import Context, Template
from importer.importer import *
from django.core.mail.backends.smtp import EmailBackend
import logging
logger = logging.getLogger("logging.StreamHandler")

class Broadcast(models.Model):
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    template = models.ForeignKey(
        MailTemplate, on_delete=models.CASCADE)
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.creation_date) + "_" + str(self.agenda) + "_" + str(self.template)

    def send(self, engine, user, password):
        template = Template( self.template.content)
        subject = Template(self.template.subject)
        agenda = self.agenda
        mails = []
        contacts = [removeState(fromContactToDict(contact)) for contact in Contact.objects.filter(agenda=agenda)]
        for contact in contacts:
            mail_subject = subject.render(Context(contact["contact_info"]))
            mail_content = template.render(Context(contact["contact_info"]))
            mails.append((mail_subject, mail_content, None, [contact["email"]]))
            
        backend=self.engine(engine, user, password)
        backend.open()
        send_mass_mail(mails, auth_user=user, auth_password=password, connection=backend)

    def engine(self,x, user, password):
        return {'gmail':EmailBackend(host="smtp.gmail.com", port=465, use_ssl=True, username=user, password=password)}[x]