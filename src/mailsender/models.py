from django.db import models
from contacts.models import Contact
from django.template import Template
from .helpers import send_mass_html_mail, createMails


class ResultadoDifusion(models.Model):
    contacto = models.ForeignKey(
        Contact, on_delete=models.CASCADE, blank=True, null=True
    )
    resultado_del_envio = models.BooleanField()


class MassMail(models.Model):
    subject = models.CharField(
        max_length=100, default="", blank=True, verbose_name="Asunto"
    )
    content = models.TextField(blank=True, default="", verbose_name="Cuerpo")
    recipients = models.ManyToManyField(Contact, verbose_name="Destinatarios")
    creation_date = models.DateField(auto_now_add=True)
    # results = models.ArrayField(
    #     models.ForeignKey(ResultadoDifusion),
    #     on_delete=models.CASCADE,
    #     blank=True,
    #     null=True,
    # )

    def __str__(self):
        return str(self.creation_date) + "_" + str(self.subject)

    def send(
        self,
        sender_email,
        sender_user,
        sender_password,
        smtp_server="correo.ugr.es",
        smtp_port=587,
    ):
        template = Template(self.content)
        subject = Template(self.subject)
        contacts = self.recipients.all()

        return send_mass_html_mail(
            createMails(template, subject, contacts, sender_user),
            sender_email,
            sender_user,
            sender_password,
            smtp_server,
            smtp_port,
        )
