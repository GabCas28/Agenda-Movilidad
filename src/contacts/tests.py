from django.test import TestCase
from .models import Contact, Agenda

class ContactTestCase(TestCase):
    def setUp(self):
        self.agenda = Agenda.objects.create(name="test_agenda")
        self.contact1 = Contact.objects.create(
            email="test1@example.com",
            agenda=self.agenda,
            contact_info={"name": "John", "phone": "1234567890"}
        )
        self.contact2 = Contact.objects.create(
            email="test2@example.com",
            agenda=self.agenda,
            contact_info={"name": "Jane", "address": "123 Main St"}
        )

    def test_create_contact(self):
        contact_info = {"name": "Bob", "email": "test3@example.com"}
        contact = Contact.create(contact_info, self.agenda, contact_info["email"])
        self.assertEqual(contact.contact_info, contact_info)
        self.assertEqual(contact.agenda, self.agenda)
        self.assertEqual(contact.email, "test3@example.com")

    def test_get_headers(self):
        headers = self.contact1.getHeaders()
        self.assertIn("name", headers)
        self.assertIn("phone", headers)
        self.assertNotIn("address", headers)

        headers = self.contact2.getHeaders()
        self.assertIn("name", headers)
        self.assertIn("address", headers)
        self.assertNotIn("phone", headers)