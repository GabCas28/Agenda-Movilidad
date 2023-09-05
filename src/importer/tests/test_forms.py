from django.test import TestCase
from ..forms import UploadFileForm
from django.core.files.uploadedfile import SimpleUploadedFile

class UploadFileFormTestCase(TestCase):
    # def test_valid_form(self):
    #     # Create form data with valid input
    #     mock_file_content = b'This is a mock Excel file content.'
    #     mock_file = SimpleUploadedFile("mock_file.xlsx", mock_file_content)

    #     form_data = {
    #         'email_header': 'Email',
    #         'file': mock_file
    #     }
    #     form = UploadFileForm(data=form_data)
    #     self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        # Create form data with invalid input
        form_data = {
            'email_header': '',  # Empty email_header is invalid
            'file': None,
            'reset': 'invalid',  # Invalid value for reset
        }
        form = UploadFileForm(data=form_data)
        
        # Check if the form is not valid
        self.assertFalse(form.is_valid())
