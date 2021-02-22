from django import forms

class UploadFileForm(forms.Form):
    email_header = forms.CharField(max_length=50)
    file = forms.FileField()