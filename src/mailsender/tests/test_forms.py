from django.test import TestCase
from ..models import MassMail
from ..forms import MassMailForm
from agendas.models import Agenda
from mailtemplates.models import MailTemplate

class MassMailFormTestCase(TestCase):
    def setUp(self):
        self.category = Agenda.objects.create(title='Test Category', slug='test-category')
        self.template = MailTemplate.objects.create(title='Test Template', slug='test-template')

    def test_mass_mail_form_valid(self):
        data = {
            'sender_name': 'Test Sender',
            'sender_email': 'test@example.com',
            'sender_user': 'smtp_username',
            'sender_password': 'smtp_password',
            'smtp_server': 'smtp.example.com',
            'smtp_port': 587,
            'content': 'Test Content',
            'recipients': [],  # Add recipients here if needed
            'agenda': self.category.slug,
            'template': self.template.slug,
        }

        form = MassMailForm(data=data, category=self.category, headers=[])
        self.assertTrue(form.is_valid())

    def tearDown(self):
        self.category.delete()
        self.template.delete()
