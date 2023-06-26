from django.contrib.admin.views.decorators import staff_member_required

from django.shortcuts import render
from .models import MassMail
from .forms import MassMailForm
from agendas.models import Agenda
from mailtemplates.models import MailTemplate
from contacts.models import Contact
from django.contrib.auth.decorators import login_required, user_passes_test


def is_superuser(user):
    return user.is_superuser


@login_required
@user_passes_test(is_superuser, login_url="accounts:staff_only")
def form(request, broadcast=""):
    def get_or_post(param):
        if request.GET.get(param):
            return request.GET.get(param)
        elif request.POST.get(param):
            return request.POST.get(param)
        else:
            return None

    broadcast = MassMail.objects.get(id=broadcast) if broadcast else None
    agenda_slug = get_or_post("agenda")
    template_slug = get_or_post("template")
    maintain = get_or_post("maintain")
    agenda = Agenda.objects.get(slug=agenda_slug) if agenda_slug else None
    category = agenda.category if agenda else None
    template = MailTemplate.objects.get(slug=template_slug) if template_slug else None

    subject = template.subject if template else None
    content = template.content if template else None
    contacts = Contact.objects.filter(agenda=agenda) if agenda else []
    headers = contacts[0].getHeaders() if contacts else []

    if request.method == "POST":
        form = MassMailForm(
            request.POST or None, instance=broadcast, category=category, headers=headers
        )
        if form.is_valid() and "import" not in request.POST:
            broadcast_instance = form.save()
            result = broadcast_instance.send(
                sender_email=request.POST["sender_email"],
                sender_user=request.POST["sender_user"],
                sender_password=request.POST["sender_password"],
                smtp_port=request.POST["smtp_port"],
                smtp_server=request.POST["smtp_server"],
            )
            return success(request, broadcast_instance.id, result)
        elif "import" in request.POST:
            if template:
                form.cleaned_data["subject"] = subject
                form.cleaned_data["content"] = content
                form.cleaned_data["template"] = None
            if agenda:
                if "recipients" in form.cleaned_data and maintain:
                    form.cleaned_data["recipients"] = form.cleaned_data[
                        "recipients"
                    ].union(contacts)
                    form.cleaned_data["maintain"] = None
                else:
                    form.cleaned_data["recipients"] = contacts

                form.cleaned_data["agenda"] = None

            form = MassMailForm(form.cleaned_data, category=category, headers=headers)

    else:
        form = MassMailForm()
    return render(
        request,
        "mailsender/form.html",
        {"broadcast": broadcast, "form": form, "form_list": list(form)},
    )


def success(request, broadcast="", result=[]):
    broadcast = MassMail.objects.get(id=broadcast) if broadcast else None
    return render(
        request, "mailsender/success.html", {"broadcast": broadcast, "result": result}
    )


@staff_member_required(login_url="accounts:staff_only")
def history(request):
    broadcasts = MassMail.objects.all()
    return render(request, "mailsender/history.html", {"broadcasts": broadcasts})
