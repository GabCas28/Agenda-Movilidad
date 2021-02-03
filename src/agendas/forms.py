from django.forms import ModelForm
from .models import Agenda

class AgendaForm(ModelForm):
     class Meta:
         model = Agenda
         fields = '__all__'