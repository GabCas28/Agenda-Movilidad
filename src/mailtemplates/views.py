from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from .models import MailTemplate, Category
from . import forms
from django.core import serializers
from django.forms import model_to_dict
import logging

# Get an instance of a logger
logger = logging.getLogger("logging.StreamHandler")


@staff_member_required(login_url="accounts:staff_only")
def deleteCategory(request, category_id):
    category = Category.objects.get(id=category_id)
    category.delete()
    return redirect("templates:home")


@staff_member_required(login_url="accounts:staff_only")
def delete(request, template_id):
    template = MailTemplate.objects.delete(id=template_id)
    template.delete()
    return redirect("templates:list")


# def categories(request):
#     categories = Category.objects.all()
#     return render(
#         request, "mailtemplates/categories/list.html", {"categories": categories}
#     )


def template_list(request):
    category = request.GET.get("category") or None
    if category:
        category = Category.objects.get(slug=category)
        templates = MailTemplate.objects.filter(category=category.id)
    else:
        templates = MailTemplate.objects.all()
    return render(
        request,
        "mailtemplates/list.html",
        {"templates": templates, "category": category},
    )


@staff_member_required(login_url="accounts:staff_only")
def template_detail(request, slug):
    template = MailTemplate.objects.get(slug=slug)
    menu_items = [
        {
            "label": cat,
            "value": [ag for ag in MailTemplate.objects.filter(category=cat.id)],
        }
        for cat in Category.objects.all()
    ]
    return render(
        request,
        "mailtemplates/detail.html",
        {
            "template": template,
            "menu_items": menu_items,
            "menu_title": "Modelos",
            "menu_type": "plantilla",
        },
    )


@staff_member_required(login_url="accounts:staff_only")
def template_form(request, slug=""):
    template = MailTemplate.objects.get(slug=slug) if slug else None
    menu_items = [
        {
            "label": cat,
            "value": [ag for ag in MailTemplate.objects.filter(category=cat.id)],
        }
        for cat in Category.objects.all()
    ]
    if request.method == "POST":
        logger.info("POST form")
        form = forms.TemplateForm(request.POST or None, instance=template)
        logger.info(form)
        if form.is_valid():
            template_instance = form.save(commit=False)
            template_instance.save()
            return redirect("templates:home")
    else:
        form = forms.TemplateForm(initial=model_to_dict(template) if template else None)
    return render(
        request,
        "mailtemplates/form.html",
        {
            "template": template,
            "form": form,
            "menu_items": menu_items,
            "menu_title": "Modelos",
            "menu_type": "plantilla",
        },
    )


@staff_member_required(login_url="accounts:staff_only")
def category_form(request, category=""):
    category = Category.objects.get(slug=category) if category else None
    if request.method == "POST":
        form = forms.CategoryForm(request.POST or None, instance=category)
        if form.is_valid():
            category_instance = form.save(commit=False)
            category_instance.save()
            return redirect("templates:home")
    else:
        form = forms.CategoryForm(initial=model_to_dict(category) if category else None)
    return render(
        request,
        "mailtemplates/categories/form.html",
        {"category": category, "form": form},
    )
