from django.shortcuts import render
from .models import Contact
from .forms import ContactForm

def contact_list(request):
    contacts = Contact.objects.all().order_by('year')
    return render(request, "contacts/contact_list.html", {"contacts":contacts})

def contact_detail(request, contact_id):
    contact = Contact.objects.get(id=contact_id)
    return render(request, "contacts/contact_form.html", {"contact":contact, "form":ContactForm})