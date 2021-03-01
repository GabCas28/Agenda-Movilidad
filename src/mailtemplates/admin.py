from django.contrib import admin
from .models import MailTemplate, Category

admin.site.register(MailTemplate)
admin.site.register(Category)