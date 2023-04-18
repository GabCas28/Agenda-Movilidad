from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from .models import Contact
from agendas.models import Agenda
from . import forms
import logging
from django.core import serializers
from importer.importer import extract_headers
import json

logger = logging.getLogger("logging.StreamHandler")


@login_required
def delete(request, slug, contact_id):
    contact = Contact.objects.get(id=contact_id)
    agenda = contact.agenda
    contact.delete()
    return redirect("agendas:detail", agenda.slug)


@login_required
def contact_list(request):
    contacts = Contact.objects.all()
    contacts = [model_to_dict(contact) for contact in contacts]
    return render(
        request,
        "contacts/list.html",
        {"contacts": contacts, "headers": extract_headers(contacts)},
    )


@login_required
def contact_detail(request, contact_id):
    contact = Contact.objects.get(id=contact_id)
    return render(request, "contacts/form.html", {"contact": contact})


@login_required
def contact_form(request, slug, contact_id=""):
    contact = Contact.objects.get(id=contact_id) if contact_id else None
    try:
        agenda = Agenda.objects.get(id=slug)
    except:
        agenda = Agenda.objects.get(slug=slug)
    logger.info("form")
    if request.method == "POST":
        logger.info("POST form")
        form = forms.ContactForm(request.POST or None, instance=contact)
        if form.is_valid():
            # save game to database
            logger.info("IS VALID")
            contact_instance = form.save(commit=False)
            contact_instance.save()
            return redirect("agendas:detail", agenda.slug)
    else:
        contacts = Contact.objects.filter(agenda=agenda)
        headers = contacts[0].getHeaders() if contacts else []
        if contact:
            form = forms.ContactForm(request.POST or None, instance=contact)
        else:
            form = forms.ContactForm(
                {
                    "email": "",
                    "agenda": agenda.id,
                    "contact_info": json.dumps(dict.fromkeys(headers)),
                }
            )
    return render(
        request,
        "contacts/form.html",
        {"contact": contact, "form": form, "agenda": agenda},
    )
