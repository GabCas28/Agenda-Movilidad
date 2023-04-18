from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .importer import *
from contacts.models import Contact
from agendas.models import Agenda
from .models import Changes
from django.contrib.auth.decorators import login_required


@login_required
def accept_changes(request, slug, identifier):
    changes = Changes.objects.get(id=identifier)
    updates = [fromDictToContact(element) for element in changes.updates]
    additions = [fromDictToContact(element) for element in changes.additions]
    deletions = [fromDictToContact(element) for element in changes.deletions]

    for contact in deletions:
        Contact.objects.get(id=contact.id).delete()
    Contact.objects.bulk_update(updates, ["email", "contact_info"])
    Contact.objects.bulk_create(additions)
    return redirect("agendas:detail", slug=slug)


def classifyContacts(agenda, email_header, contacts, deletions):
    new_contacts = []
    updates = []
    new_deletions = []
    for i in range(len(contacts)):
        contact_info = contacts[i]
        email = findEmail(contact_info, email_header)
        new_contact = Contact.create(contact_info, agenda, email)
        try:
            contact = Contact.objects.get(agenda=agenda, email=email)
            if contact.contact_info != new_contact.contact_info:
                contact.contact_info = new_contact.contact_info
                contact = fromContactToDict(contact)
                prepareAndAppend(updates, contact)
            elif contact in deletions:
                contact = fromContactToDict(contact)
                prepareAndAppend(new_contacts, contact)
        except:
            contact = fromContactToDict(new_contact)
            prepareAndAppend(new_contacts, contact)

    new_deletions = []
    for delete in deletions:
        delete = fromContactToDict(delete)
        prepareAndAppend(new_deletions, delete)
    return new_contacts, updates, new_deletions


@login_required
def upload_file(request, slug):
    agenda = Agenda.objects.get(slug=slug)
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            email_header = form.data["email_header"]
            reset = form.data["reset"] if "reset" in form.data else False
            deletions = Contact.objects.filter(agenda=agenda) if reset else []

            contacts = getContactsFromFile(request.FILES["file"], email_header)
            new_contacts, updates, deletions = classifyContacts(
                agenda, email_header, contacts, deletions
            )

            changes = Changes.create(
                user=request.user,
                updates=updates,
                additions=new_contacts,
                deletions=deletions,
            )
            changes.save()
            return render(
                request,
                "importer/changes.html",
                {
                    "new_contacts": new_contacts,
                    "keys_new_contacts": extract_headers(new_contacts),
                    "duplicates": updates,
                    "keys_duplicates": extract_headers(updates),
                    "deletions": deletions,
                    "keys_deletions": extract_headers(deletions),
                    "agenda": agenda,
                    "changes": changes,
                },
            )
    else:
        form = UploadFileForm()
    return render(request, "agendas/detail.html", {"form": form})
