from django.forms import ModelForm, Form, CharField, FileField
from .models import Category, MailTemplate

class TemplateForm(ModelForm):
     class Meta:
         model = MailTemplate
         fields = '__all__'

class CategoryForm(ModelForm):
     class Meta:
         model = Category
         fields = '__all__'