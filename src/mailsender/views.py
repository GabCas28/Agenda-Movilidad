from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import MassMail
from .forms import MassMailForm
from django.core.exceptions import ValidationError
from agendas.models import Agenda
from mailtemplates.models import MailTemplate
from contacts.models import Contact
import re

@login_required
def form(request, broadcast=""):

    def get_or_post(param):
        print(param)
        print(param)
        print(request.GET)
        print(request.POST)
        if request.GET.get(param):
            return request.GET.get(param)
        elif request.POST.get(param):
            return request.POST.get(param)
        else:
            return None

    broadcast = MassMail.objects.get(id=broadcast) if broadcast else None
    agenda_slug = get_or_post("agenda")
    template_slug = get_or_post("template")
    agenda= Agenda.objects.get(slug=agenda_slug) if agenda_slug else None
    template=MailTemplate.objects.get(slug=template_slug) if template_slug else None
    print("agenda",agenda)
    print("template", template)
    
    subject = template.subject if template else None
    content = template.content if template else None
    contacts = Contact.objects.filter(agenda=agenda) if agenda else None

    if request.method == "POST":
        form= MassMailForm(request.POST or None, instance=broadcast)
        if form.is_valid() and 'import' not in request.POST:
            broadcast_instance=form.save()
            user = request.POST["user"]
            broadcast_instance.send(user=user, password=request.POST["password"])
            return redirect('sender:success', broadcast_instance.id)
        elif 'import' in request.POST:
            if template:
                form.cleaned_data['subject'] = subject
                form.cleaned_data['content'] = content
                form.cleaned_data['template'] = None
            if agenda:
                if 'recipients' in form.cleaned_data and 'maintain' in form.cleaned_data:
                    form.cleaned_data['recipients'] = form.cleaned_data['recipients'].union(contacts)
                    form.cleaned_data['maintain'] = None
                else:
                    form.cleaned_data['recipients'] = contacts
                
                form.cleaned_data['agenda'] = None
            form= MassMailForm(form.cleaned_data)

    else: 
        form= MassMailForm({"recipients": contacts, "subject":subject, "content":content})
    return render(request, "mailsender/form.html", {"broadcast": broadcast, "form" : form, "form_list": list(form)})



def success(request, broadcast=""):
    broadcast = MassMail.objects.get(id=broadcast) if broadcast else None
    return render(request, "mailsender/success.html", {"broadcast": broadcast})


@login_required
def history(request):
    broadcasts = MassMail.objects.all()
    return render(request, "mailsender/history.html", {"broadcasts": broadcasts})
