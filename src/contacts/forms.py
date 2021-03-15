from django.forms import ModelForm
from .models import Contact
from django_json_widget.widgets import JSONEditorWidget

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
            'contact_info':JSONEditorWidget(),
        }