from typing import Text
from django.forms import ModelForm, Form
from django.forms.fields import BooleanField, CharField, EmailField, ChoiceField
from django.forms.widgets import PasswordInput
from .models import  MassMail
from django_summernote.widgets import SummernoteWidget
from django.contrib.admin.widgets import FilteredSelectMultiple
from agendas.models import Agenda
from mailtemplates.models import MailTemplate

class MassMailForm(ModelForm):
    user= CharField(required=True)
    password = CharField(widget=PasswordInput())
    agendas=[(agenda.slug, agenda.__str__) for agenda in Agenda.objects.all()]
    templates=[(template.slug, template.__str__) for template in MailTemplate.objects.all()]
    agendas.insert(0,(None,"---"))
    templates.insert(0,(None,"---"))
    agenda = ChoiceField(choices=agendas, required = False, label="Agenda")
    template = ChoiceField(choices=templates, required = False, label="Plantilla")
    maintain = BooleanField(required=False, label="Conservar contactos existentes")
    class Meta:
        model = MassMail
        fields = ['subject', 'recipients', 'content','user', 'password', 'agenda', 'maintain', 'template']
        widgets = {
            'content': SummernoteWidget(),
            'recipients': FilteredSelectMultiple("contacts", is_stacked=False),
        }
    class Media:
        css = {
            'all': ('/static/admin/css/widgets.css', '/static/css/styles.css'),
        }
        js = ('/admin/jsi18n',)

# class RecipientsForm(ModelForm):
#     agenda=ChoiceField(choices=[(agenda.id, agenda.__str__) for agenda in Agenda.objects.all()], required = False)

# class TemplateForm(ModelForm):
#     template=ChoiceField(choices=[(template.id, template.__str__) for template in MailTemplate.objects.all()], required = False)