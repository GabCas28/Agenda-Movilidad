from django.test import TestCase
from ..models import Contact
from agendas.models import Agenda, Category
from django.db import IntegrityError

class ContactModelTestCase(TestCase):
    def setUp(self):
        # Create a test category and agenda
        self.category = Category.objects.create(title='Test Category', slug='test-category')
        self.agenda = Agenda.objects.create(title='Test Agenda', slug='test-agenda', category=self.category, year=2023)

    def test_create_contact(self):
        # Create a new Contact object
        email = 'test@example.com'
        contact_info = {'name': 'Test Name', 'phone': '123-456-7890'}
        contact = Contact.create(contact_info=contact_info, agenda=self.agenda, email=email)

        # Check if the object was created successfully
        self.assertEqual(contact.email, email)
        self.assertEqual(contact.contact_info, contact_info)
        self.assertEqual(contact.agenda, self.agenda)

    def test_model_str_method(self):
        # Create a Contact object
        email = 'test@example.com'
        contact_info = {'name': 'Test Name', 'phone': '123-456-7890'}
        contact = Contact.create(contact_info=contact_info, agenda=self.agenda, email=email)

        # Check the string representation of the Contact object
        expected_str = f'{self.agenda}: {email}'
        self.assertEqual(str(contact), expected_str)

    # def test_model_unique_constraint(self):
    #     # Create a Contact object
    #     email = 'test@example.com'
    #     contact_info = {'name': 'Test Name', 'phone': '123-456-7890'}
    #     Contact.create(contact_info=contact_info, agenda=self.agenda, email=email)

    #     # Attempt to create another Contact with the same email and agenda (should raise IntegrityError)
    #     with self.assertRaises(IntegrityError):
    #         Contact.create(contact_info=contact_info, agenda=self.agenda, email=email)

    def tearDown(self):
        # Clean up (delete the test category and agenda)
        self.category.delete()
        self.agenda.delete()
