from django.forms import ModelForm, CharField
from django.forms.widgets import PasswordInput
from .models import Broadcast

class BroadcastForm(ModelForm):
    user = CharField(max_length=100)
    password = CharField(widget=PasswordInput)
    class Meta:
        model = Broadcast
        fields = '__all__'