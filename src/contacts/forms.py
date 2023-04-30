from django.forms import ModelForm
from .models import Contact
from django_json_widget.widgets import JSONEditorWidget
from django.utils.text import slugify
from importer.views import snake_case

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
            'contact_info':JSONEditorWidget(),
        }
    
    class Media:
        css = {
            'all': ('/static/css/styles.css'),
        }

    def save(self, commit=True):
        instance = super(ContactForm, self).save(commit=False)
        
        contact_info = instance.contact_info
        updated_contact_info = {}
        for key, value in contact_info.items():
            updated_key = snake_case(key)
            updated_contact_info[updated_key] = value
            
        instance.contact_info = updated_contact_info

        if commit:
            instance.save()

        return instance