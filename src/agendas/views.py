from django.shortcuts import render
from .models import Agenda
from contacts.models import Contact

def agenda_list(request):
    agendas = Agenda.objects.all().order_by('year')
    return render(request, "agendas/agendas.html", {"agendas":agendas})

def agenda_detail(request, slug):
    agenda = Agenda.objects.get(slug=slug)
    contacts = Contact.objects.filter(agenda=agenda)
    return render(request, "agendas/agenda_detail.html", {"agenda":agenda, "contacts": contacts})