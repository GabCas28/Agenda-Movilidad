from django.shortcuts import render, redirect
from .models import MailTemplate, Category
from . import forms
from django.core import serializers
import logging
# Get an instance of a logger
logger = logging.getLogger("logging.StreamHandler")

def categories(request):
    categories = Category.objects.all()
    return render(request, "mailtemplates/categories/list.html", {"categories":categories})

def template_list(request, category=""):
    if category:
        category = Category.objects.get(slug=category)
        templates = MailTemplate.objects.filter(category=category.id)
    else:
        templates= MailTemplate.objects.all()    
    return render(request, "mailtemplates/list.html", {"templates":templates})

def template_detail(request, slug):
    template = MailTemplate.objects.get(slug=slug)
    return render(request, "mailtemplates/detail.html", {"template":template})

def template_form(request, template=''):
    template = MailTemplate.objects.get(id=template) if template else None
    logger.info("form")
    if request.method=="POST":
        logger.info("POST form")
        form = forms.TemplateForm(request.POST or None, instance=template)
        logger.info(form)
        if form.is_valid():
            template_instance = form.save(commit=False)
            template_instance.save()
            return redirect('templates:home')
    else:
        form = forms.TemplateForm(initial=template.__dict__ if template else None)
    return render(request, "mailtemplates/form.html", {"template":template,"form":form})


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
            return redirect('templates:home')
    else:
        form = forms.CategoryForm(initial=category.__dict__ if category else None)
    return render(request, "mailtemplates/categories/form.html", {"category":category,"form":form})
