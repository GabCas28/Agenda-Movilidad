from django.contrib import admin
from .models import MailTemplate, Category
from django_summernote.admin import SummernoteModelAdmin

class MailTemplateAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'

admin.site.register(MailTemplate,MailTemplateAdmin)
admin.site.register(Category)