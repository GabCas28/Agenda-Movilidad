from django.shortcuts import render, redirect
from .models import Agenda
from contacts.models import Contact
from . import forms
from django.core import serializers
import logging
from importer.forms import UploadFileForm
# Get an instance of a logger
logger = logging.getLogger("logging.StreamHandler")

def agenda_list(request):
    agendas = Agenda.objects.all().order_by('year')
    return render(request, "agendas/agendas.html", {"agendas":agendas})

def agenda_detail(request, slug):
    agenda = Agenda.objects.get(slug=slug)
    contacts = Contact.objects.filter(agenda=agenda)
    form = UploadFileForm()
    if contacts:
        headers= list(contacts[0].contact_info.keys())
    return render(request, "agendas/agenda_detail.html", {"agenda":agenda, "contact_list": contacts, "form":form, "headers":headers, "len_headers":len(headers)})

def agenda_form(request, agenda_id='new'):
    agenda = Agenda.objects.get(id=agenda_id) if agenda_id!="new" else None
    logger.info("form")
    if request.method=="POST":
        logger.info("POST form")
        form = forms.AgendaForm(request.POST or None, instance=agenda)
        logger.info(form)
        if form.is_valid():
            #save game to database
            contact_instance = form.save(commit=False)
            contact_instance.save()
            return redirect('agendas:home')
    else:
        form = forms.AgendaForm(initial=agenda.__dict__ if agenda_id!="new" else None)
    return render(request, "agendas/agenda_form.html", {"agenda":agenda,"form":form})

