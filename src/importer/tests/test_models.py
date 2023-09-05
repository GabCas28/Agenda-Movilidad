from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Changes

class ChangesModelTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_create_changes(self):
        # Create a Changes instance
        changes = Changes.create(
            user=self.user,
            old_state={'key1': 'value1'},
            updates={'key2': 'value2'},
            additions={'key3': 'value3'},
            deletions={'key4': 'value4'}
        )

        # Check if the Changes instance was created successfully
        self.assertIsInstance(changes, Changes)
        self.assertEqual(changes.user, self.user)
        self.assertEqual(changes.old_state, {'key1': 'value1'})
        self.assertEqual(changes.updates, {'key2': 'value2'})
        self.assertEqual(changes.additions, {'key3': 'value3'})
        self.assertEqual(changes.deletions, {'key4': 'value4'})

    def test_create_changes_default_values(self):
        # Create a Changes instance with default values
        changes = Changes.create(user=self.user)

        # Check if the Changes instance was created with default values
        self.assertIsInstance(changes, Changes)
        self.assertEqual(changes.user, self.user)
        self.assertEqual(changes.old_state, {})
        self.assertEqual(changes.updates, {})
        self.assertEqual(changes.additions, {})
        self.assertEqual(changes.deletions, {})