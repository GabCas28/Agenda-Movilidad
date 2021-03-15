from django.forms import ModelForm, Form, CharField, FileField
from .models import Category, MailTemplate
from django_summernote.widgets import SummernoteWidget

class TemplateForm(ModelForm):
     class Meta:
         model = MailTemplate
         fields = '__all__'
         widgets = {
            'content': SummernoteWidget(),
         }

class CategoryForm(ModelForm):
     class Meta:
         model = Category
         fields = '__all__'