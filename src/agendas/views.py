from django.shortcuts import render

def agenda_list(request):
    return render(request, "agendas/agendas.html")