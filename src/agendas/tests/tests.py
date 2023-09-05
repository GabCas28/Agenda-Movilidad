from django.test import TestCase
from ..models import Agenda, Category
# from django.db import transaction


class AgendaModelTestCase(TestCase):
    def setUp(self):
        # Create a test category
        self.category = Category.objects.create(title='Test Category', slug='test-category')

    def test_create_agenda(self):
        # Create a new Agenda object
        title = 'Test Agenda'
        year = 2023
        agenda = Agenda.objects.create(title=title, slug='test-agenda', category=self.category, year=year)

        # Check if the object was created successfully
        self.assertEqual(agenda.title, title)
        self.assertEqual(agenda.category, self.category)
        self.assertEqual(agenda.year, year)

    def test_model_str_method(self):
        # Create an Agenda object
        title = 'Test Agenda'
        year = 2023
        agenda = Agenda.objects.create(title=title, slug='test-agenda', category=self.category, year=year)

        # Check the string representation of the Agenda object
        expected_str = f'{year}-{self.category}-{title}'
        self.assertEqual(str(agenda), expected_str)

    # def test_model_unique_together_constraint(self):
    #     # Create two agendas with the same slug and category (should raise IntegrityError)
    #     title = 'Test Agenda'
    #     agenda1 = Agenda.objects.create(title=title, slug='test-agenda', category=self.category, year=2023)
    #     with self.assertRaises(Exception):
    #         agenda2 = Agenda.objects.create(title=title, slug='test-agenda', category=self.category, year=2024)
    #         agenda2.b

    # @transaction.atomic
    def tearDown(self):
        # # Delete all agendas associated with the test category
        # Agenda.objects.filter(category=self.category).delete()

        # Clean up (delete the test category)
        self.category.delete()
