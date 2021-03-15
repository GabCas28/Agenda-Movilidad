from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from .models import Contact
from . import forms
import logging
from django.core import serializers
from importer.importer import extractHeaders

logger = logging.getLogger("logging.StreamHandler")

def contact_list(request):
    contacts = Contact.objects.all()
    contacts = [model_to_dict(contact) for contact in contacts]
    return render(request, "contacts/list.html", {"contacts": contacts, "headers":extractHeaders(contacts)})

def contact_detail(request, contact_id):
    contact = Contact.objects.get(id=contact_id)
    return render(request, "contacts/form.html", {"contact":contact})

def contact_form(request, contact_id=''):
    contact = Contact.objects.get(id=contact_id) if contact_id else None
    logger.info("form")
    if request.method=="POST":
        logger.info("POST form")
        form = forms.ContactForm(request.POST or None, instance=contact)
        if form.is_valid():
            #save game to database
            logger.info("IS VALID")
            contact_instance = form.save(commit=False)
            contact_instance.save()
            return redirect('contacts:list')
    else:
        form = forms.ContactForm(instance=contact if contact_id else None)
    return render(request, "contacts/form.html", {"contact":contact,"form":form})
