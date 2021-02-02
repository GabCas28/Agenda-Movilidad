from django.shortcuts import render
from .models import Agenda

def agenda_list(request):
    agendas = Agenda.objects.all().order_by('year')
    return render(request, "agendas/agendas.html", {"agendas":agendas})

def agenda_detail(request, slug):
    agenda = Agenda.objects.get(slug=slug)
    return render(request, "agendas/agenda_detail.html", {"agenda":agenda})