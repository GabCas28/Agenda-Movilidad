from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from .models import Agenda, Category
from contacts.models import Contact
from . import forms
from django.core import serializers
from importer.forms import UploadFileForm
from importer.importer import extractHeaders

# Get an instance of a logger
import logging

logger = logging.getLogger("logging.StreamHandler")
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from agendas.serializers import AgendaSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser


def categories(request):
    categories = Category.objects.all()
    return render(request, "agendas/categories/list.html", {"categories": categories})


def agenda_list(request):
    category = request.GET.get("category") or None
    if category:
        category = Category.objects.get(slug=category)
        agendas = Agenda.objects.filter(category=category.id).order_by("year")

        return render(
            request, "agendas/list.html", {"agendas": agendas, "category": category}
        )
    else:
        agendas = Agenda.objects.all()
    return render(request, "agendas/list.html", {"agendas": agendas})


def get_agendas(request):
    agendas = Agenda.objects.all()
    serializer = AgendaSerializer(agendas, many=True)
    return JsonResponse(serializer.data, safe=False)
    # return render(request, "agendas/list.html", {"agendas":agendas})


@login_required
def agenda_detail(request, slug=None):
    agenda = Agenda.objects.get(slug=slug) if slug else None
    contacts = (
        [model_to_dict(contact) for contact in Contact.objects.filter(agenda=agenda)]
        if slug
        else [model_to_dict(contact) for contact in Contact.objects.all()]
    )
    menu_items = [
        {"label": cat, "value": [ag for ag in Agenda.objects.filter(category=cat)]}
        for cat in Category.objects.all()
    ]
    form = UploadFileForm()
    headers = extractHeaders(contacts)
    return render(
        request,
        "agendas/detail.html",
        {
            "agenda": agenda,
            "contact_list": contacts,
            "form": form,
            "headers": headers,
            "len_headers": len(headers),
            "menu_items": menu_items,
            "menu_title": 'Agendas',
            "menu_type": 'agenda',
        },
    )


@login_required
def agenda_form(request, slug=""):
    category = request.GET.get("category") or None
    agenda = Agenda.objects.get(slug=slug) if slug else None
    logger.info("form")
    if request.method == "POST":
        logger.info("POST form")
        form = forms.AgendaForm(request.POST or None, instance=agenda)
        logger.info(form)
        if form.is_valid():
            contact_instance = form.save(commit=False)
            contact_instance.save()
            return redirect("agendas:home")
    else:

        if category:
            category = Category.objects.get(slug=category)
            form = forms.AgendaForm(
                {"title": "", "slug": "", "year": "", "category": category.id}
            )
        else:
            form = forms.AgendaForm(initial=model_to_dict(agenda) if agenda else None)
    return render(request, "agendas/form.html", {"agenda": agenda, "form": form})


@login_required
def category_form(request, category=""):
    category = Category.objects.get(slug=category) if category else None
    logger.info("form")
    if request.method == "POST":
        logger.info("POST form")
        form = forms.CategoryForm(request.POST or None, instance=category)
        logger.info(form)
        if form.is_valid():
            category_instance = form.save(commit=False)
            category_instance.save()
            return redirect("agendas:home")
    else:
        form = forms.CategoryForm(initial=model_to_dict(category) if category else None)
    return render(
        request, "agendas/categories/form.html", {"category": category, "form": form}
    )


@login_required
def deleteCategory(request, category_id):
    category = Category.objects.get(id=category_id)
    category.delete()
    return redirect("agendas:home")


@login_required
def delete(request, agenda_id):
    agenda = Agenda.objects.get(id=agenda_id)
    agenda.delete()
    return redirect("agendas:list")
