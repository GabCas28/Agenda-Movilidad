from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from ..models import Changes
from agendas.models import Agenda

class ImporterViewsTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test agenda
        self.agenda = Agenda.objects.create(slug='test-agenda')

        # Create a Changes instance for testing
        self.changes = Changes.objects.create(user=self.user)

    def test_accept_changes_view(self):
        # Define test data
        identifier = self.changes.id

        # Call the view using the reverse URL
        url = reverse('importer:accept', args=[identifier])
        response = self.client.get(url)

        # Assert the response status code and any other relevant checks
        self.assertEqual(response.status_code, 302)  # Expect a redirect

    def test_upload_file_view(self):
        # Define test data
        slug = self.agenda.slug

        # Create a mock file to upload
        mock_file_content = b'This is a mock Excel file content.'
        mock_file = SimpleUploadedFile("mock_file.xlsx", mock_file_content)

        # Create form data
        form_data = {
            'email_header': 'Email',
            'file': mock_file,
        }

        # Log in the user (since it's a login-required view)
        self.client.login(username='testuser', password='testpassword')

        # Call the view using the reverse URL with form data
        url = reverse('importer:main')
        response = self.client.post(url, data=form_data, follow=True)

        # Assert the response status code and any other relevant checks
        self.assertEqual(response.status_code, 200)  # Expect a successful response


        # Check if the Changes model was created:
        self.assertTrue(Changes.objects.filter(user=self.user).exists())

        # Clean up (delete the test user and any other created objects)
        self.user.delete()
        self.agenda.delete()
        self.changes.delete()
