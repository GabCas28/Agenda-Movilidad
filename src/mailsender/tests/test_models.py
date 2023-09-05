from django.test import TestCase
from django.core.mail import EmailMessage
from unittest.mock import patch
from ..models import MassMail
from contacts.models import Contact
from agendas.models import Agenda

class MassMailTestCase(TestCase):
    def setUp(self):
        # Create an Agenda
        self.agenda = Agenda.objects.create(
            title='Test Agenda',
            slug='test-agenda',
            year=2023,
        )

        # Create a test contact associated with the Agenda
        self.contact = Contact.objects.create(
            email='test@example.com',
            agenda=self.agenda,
        )

    def test_send_method(self):
        # Create a MassMail object
        mass_mail = MassMail.objects.create(
            subject='Test Subject',
            content='Test Content',
        )
        mass_mail.recipients.add(self.contact)

        # Define the expected sender information
        sender_name = 'Test Sender'
        sender_email = 'testsender@example.com'
        sender_user = 'smtp_username'
        sender_password = 'smtp_password'

        # Mock the send_mass_html_mail function
        with patch('mailsender.models.send_mass_html_mail') as mock_send_mail:
            # Call the send method
            result = mass_mail.send(
                sender_name=sender_name,
                sender_email=sender_email,
                sender_user=sender_user,
                sender_password=sender_password,
                smtp_server='smtp.example.com',
                smtp_port=587,
            )

        # Assert that the send_mass_html_mail function was called
        mock_send_mail.assert_called_once()


        # Assert that the result is True, indicating successful sending
        self.assertTrue(result)

    def tearDown(self):
        # Clean up by deleting the test contact and agenda
        self.contact.delete()
        self.agenda.delete()
