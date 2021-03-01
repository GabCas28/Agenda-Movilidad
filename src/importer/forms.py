from django import forms


class UploadFileForm(forms.Form):
    email_header = forms.CharField(max_length=50, label="Cabecera de email")
    file = forms.FileField(label="Archivo Excel a importar")
    reset = forms.BooleanField(label="Eliminar contactos existentes", required=False)
