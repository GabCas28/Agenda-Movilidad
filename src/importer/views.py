from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .importer import *
from contacts.models import Contact
from agendas.models import Agenda
from .models import Changes
import json

def accept_changes(request,slug, identifier):
    changes = Changes.objects.get(id=identifier)
    updates = [ fromDictToContact(element) for element in changes.updates ]
    additions = [ fromDictToContact(element) for element in changes.additions ]
    print("new_contacts",updates)
    print("duplicates",additions)
    Contact.objects.bulk_update(updates, ["email","contact_info"])
    Contact.objects.bulk_create(additions)
    return redirect("agendas:detail", slug=slug)
    

def upload_file(request, slug):
    agenda = Agenda.objects.get(slug=slug)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            email_header = form.data["email_header"]
            contacts = getContactsFromFile(request.FILES['file'], email_header)
            new_contacts, updates = classifyContacts(agenda, email_header, contacts)
            changes = Changes.create(user=request.user, updates=updates, additions=new_contacts)
            changes.save()
            return render(request, 'importer/changes.html', {"new_contacts":new_contacts, "duplicates":updates, "agenda":agenda, "changes":changes})
    else:
        form = UploadFileForm()
    return render(request, 'agendas/agenda_detail.html', {'form': form})

def classifyContacts(agenda, email_header, contacts):
    new_contacts = []
    updates = []
    for i in range(len(contacts)):
        contact_info = contacts[i]
        email = findEmail(contact_info, email_header)
        new_contact = Contact.create(contact_info, agenda, email)
        try:
            contact = Contact.objects.get(agenda=agenda,email=email)
            contact.contact_info = new_contact.contact_info
            contact = fromContactToDict(contact)
            prepareAndAppend(updates, contact)
        except: 
            contact = fromContactToDict(new_contact)
            prepareAndAppend(new_contacts, contact)
    return new_contacts,updates

