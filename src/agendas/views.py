from django.shortcuts import render, redirect
from .models import Agenda, Category
from contacts.models import Contact
from . import forms
from django.core import serializers
from importer.forms import UploadFileForm
from importer.importer import *
# Get an instance of a logger
import logging
logger = logging.getLogger("logging.StreamHandler")

def categories(request):
    categories = Category.objects.all()
    return render(request, "agendas/categories/list.html", {"categories":categories})

def agenda_list(request, category=""):
    if category:
        category=Category.objects.get(slug=category)
        agendas = Agenda.objects.filter(category=category.id).order_by('year')
    else:
        agendas= Agenda.objects.all()    
    return render(request, "agendas/list.html", {"agendas":agendas})

def agenda_detail(request, slug):
    agenda = Agenda.objects.get(slug=slug)
    contacts = [removeState(fromContactToDict(contact)) for contact in Contact.objects.filter(agenda=agenda)]
    form = UploadFileForm()
    headers = extractHeaders(contacts)
    return render(request, "agendas/detail.html", {"agenda":agenda, "contact_list": contacts, "form":form, "headers":headers, "len_headers":len(headers)})

def agenda_form(request, agenda_id='new'):
    agenda = Agenda.objects.get(id=agenda_id) if agenda_id!="new" else None
    logger.info("form")
    if request.method=="POST":
        logger.info("POST form")
        form = forms.AgendaForm(request.POST or None, instance=agenda)
        logger.info(form)
        if form.is_valid():
            contact_instance = form.save(commit=False)
            contact_instance.save()
            return redirect('agendas:home')
    else:
        form = forms.AgendaForm(initial=agenda.__dict__ if agenda_id!="new" else None)
    return render(request, "agendas/form.html", {"agenda":agenda,"form":form})


def category_form(request, category=''):
    category = Category.objects.get(slug=category) if category else None
    logger.info("form")
    if request.method=="POST":
        logger.info("POST form")
        form = forms.CategoryForm(request.POST or None, instance=category)
        logger.info(form)
        if form.is_valid():
            category_instance = form.save(commit=False)
            category_instance.save()
            return redirect('agendas:home')
    else:
        form = forms.CategoryForm(initial=category.__dict__ if category else None)
    return render(request, "agendas/categories/form.html", {"category":category,"form":form})
