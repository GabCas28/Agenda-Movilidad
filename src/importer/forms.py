from django import forms


class UploadFileForm(forms.Form):
    email_header = forms.CharField(max_length=50, label="Cabecera de la columna que contiene los correos")
    file = forms.FileField(label="Archivo Excel")
    reset = forms.BooleanField(label="Eliminar contactos existentes", required=False)
