from django.template import Template, Context
from django.test import TestCase
from ..models import createMails
from contacts.models import Contact
from agendas.models import Agenda

class CreateMailsTestCase(TestCase):
    def setUp(self):
        self.agenda = Agenda.objects.create(title='Test Agenda')
        self.contact1 = Contact.objects.create(
            email='contact1@example.com',
            contact_info={'name': 'John Doe', 'phone': '123-456-7890'},
            agenda=self.agenda
        )
        self.contact2 = Contact.objects.create(
            email='contact2@example.com',
            contact_info={'name': 'Jane Smith', 'phone': '987-654-3210'},
            agenda=self.agenda
        )
        self.template = Template("Hello {{ name }}!<br>Your phone number is {{ phone }}.")
        self.subject = Template("Test Email")

    def test_create_mails(self):
        contacts = [self.contact1, self.contact2]
        sender = 'sender@example.com'

        mails = createMails(self.template, self.subject, contacts, sender)

        self.assertEqual(len(mails), 2)

        mail1 = mails[0]
        self.assertEqual(mail1['From'], sender)
        self.assertEqual(mail1['To'], self.contact1.email)
        self.assertEqual(mail1['Subject'], 'Test Email')

        mail2 = mails[1]
        self.assertEqual(mail2['From'], sender)
        self.assertEqual(mail2['To'], self.contact2.email)
        self.assertEqual(mail2['Subject'], 'Test Email')

    def tearDown(self):
        self.contact1.delete()
        self.contact2.delete()
        self.agenda.delete()
