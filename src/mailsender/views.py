from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
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
        return request.GET.get(param) or request.POST.get(param)

    broadcast_instance = (
        get_object_or_404(MassMail, id=broadcast) if broadcast else None
    )
    import_flag = "import" in request.POST
    agenda_slug = get_or_post("agenda")
    template_slug = get_or_post("template")
    maintain = get_or_post("maintain")
    agenda = get_object_or_404(Agenda, slug=agenda_slug) if agenda_slug else None
    category = agenda.category if agenda else None
    template = (
        get_object_or_404(MailTemplate, slug=template_slug) if template_slug else None
    )

    subject = template.subject if template else None
    content = template.content if template else None
    contacts = Contact.objects.filter(agenda=agenda) if agenda else []
    headers = contacts[0].getHeaders() if contacts else []

    if request.method == "POST" and not "imported" in request.POST:
        form = MassMailForm(
            request.POST or None,
            instance=broadcast_instance,
            category=category,
            headers=headers,
        )
        if form.is_valid() and not import_flag:
            broadcast_instance = form.save()
            result = broadcast_instance.send(
                sender_name=request.POST["sender_name"],
                sender_email=request.POST["sender_email"],
                sender_user=request.POST["sender_user"],
                sender_password=request.POST["sender_password"],
                smtp_port=request.POST["smtp_port"],
                smtp_server=request.POST["smtp_server"],
            )
            return success(request, broadcast_instance.id, result)
        elif import_flag:
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
        if "imported" in request.POST:
            if agenda:
                form.initial["recipients"] = contacts
                form.initial["agenda"] = None
            if template:
                form.initial["subject"] = subject
                form.initial["content"] = content
                form.initial["template"] = None

    return render(
        request,
        "mailsender/form.html",
        {"broadcast": broadcast_instance, "form": form, "form_list": list(form)},
    )


def success(request, broadcast="", result=[]):
    broadcast_instance = (
        get_object_or_404(MassMail, id=broadcast) if broadcast else None
    )
    return render(
        request,
        "mailsender/success.html",
        {"broadcast": broadcast_instance, "result": result},
    )


@staff_member_required(login_url="accounts:staff_only")
def history(request):
    broadcasts = MassMail.objects.all()
    return render(request, "mailsender/history.html", {"broadcasts": broadcasts})
