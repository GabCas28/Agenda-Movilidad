from django.shortcuts import render, redirect
from .models import Contact
from . import forms
import logging
from django.core import serializers

logger = logging.getLogger("logging.StreamHandler")

def contact_list(request):
    contacts = Contact.objects.all()
    return render(request, "contacts/contact_list.html", {"contacts":contacts})

def contact_detail(request, contact_id):
    contact = Contact.objects.get(id=contact_id)
    return render(request, "contacts/contact_form.html", {"contact":contact})

def contact_form(request, contact_id='new'):
    contact = Contact.objects.get(id=contact_id) if contact_id!='new' else None
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
        form = forms.ContactForm(initial=contact.__dict__ if contact_id!='new' else None)
        logger.info("GET form")
        logger.info(form)
    return render(request, "contacts/contact_form.html", {"contact":contact,"form":form})