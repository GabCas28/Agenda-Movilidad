from django.db import models
from contacts.models import Contact
from django.core.mail import send_mass_mail
from django.template import Context, Template
from django.core.mail.backends.smtp import EmailBackend
import re 
import logging
logger = logging.getLogger("logging.StreamHandler")

class MassMail(models.Model):
    subject = models.CharField(max_length=100, default="", blank=True)
    content = models.TextField(blank=True, default="")
    recipients = models.ManyToManyField(Contact)
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.creation_date) + "_" + str(self.subject)

    def send(self, user, password):
        template = Template(self.content)
        subject = Template(self.subject)
        contacts = self.recipients.all()
        print("contacts",contacts)
        mails = []
        backend = None

        def html_to_text(html):
            result = re.sub('<br>','\n', html)
            result = re.sub('</p>','\n', result)
            result = re.sub('<\/?[^>]+(>|$)','', result)
            return result

        def createMails():
            for contact in contacts:
                mail_subject = subject.render(Context(contact.contact_info))
                mail_content = template.render(Context(contact.contact_info))
                mails.append((mail_subject,html_to_text(mail_content), mail_content, None, [contact.email]))
            

        def prepareBackend():

            def chooseEngine(x):
                if 'gmail' in x:
                    return 'gmail'
                elif 'ugr' in x:
                    return 'ugr'
                else:
                    return 'ugr'

            def engine(x,user, password):
                return {'gmail':EmailBackend(host="smtp.gmail.com", port=465, use_ssl=True, username=user, password=password), 
                'ugr':EmailBackend(host="correo.ugr.es", port=465 , use_ssl=True, username=user, password=password)}[x]

            backend=engine(chooseEngine(user), user, password)
            backend.open()
        
        
        createMails()
        prepareBackend()
        send_mass_html_mail(mails, auth_user=user, auth_password=password, connection=backend)

        

from django.core.mail import get_connection, EmailMultiAlternatives

def send_mass_html_mail(datatuple, fail_silently=False, auth_user=None, auth_password=None, 
                        connection=None):
    """
    Given a datatuple of (subject, text_content, html_content, from_email,
    recipient_list), sends each message to each recipient list. Returns the
    number of emails sent.

    If from_email is None, the DEFAULT_FROM_EMAIL setting is used.
    If auth_user and auth_password are set, they're used to log in.
    If auth_user is None, the EMAIL_HOST_USER setting is used.
    If auth_password is None, the EMAIL_HOST_PASSWORD setting is used.

    """
    connection = connection or get_connection(
        username=auth_user, password=auth_password, fail_silently=fail_silently)
    messages = []
    for subject, text, html, from_email, recipient in datatuple:
        message = EmailMultiAlternatives(subject, text, from_email, recipient)
        message.attach_alternative(html, 'text/html')
        messages.append(message)
    return connection.send_messages(messages)