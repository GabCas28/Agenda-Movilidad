from django.contrib import admin
from .models import Contact
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget

class MyAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField:{ 'widget':JSONEditorWidget },
    }
admin.site.register(Contact, MyAdmin)