from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import MassMail
from .forms import MassMailForm
from django.core.exceptions import ValidationError
from agendas.models import Agenda
from mailtemplates.models import MailTemplate
from contacts.models import Contact
from django.http import HttpResponse
import csv
from win32com import client
import pythoncom
import os, sys
import gzip

PST_FILEPATH = os.path.abspath(
    os.path.join(os.path.expandvars("%APPDATA%"), "scratch.pst")
)


@login_required
def form(request, broadcast=""):
    # application = win32com.client.gencache.EnsureDispatch('Outlook.Application', pythoncom.CoInitialize())
    # application.Visible = True
    # application = win32com.client.Dispatch("Outlook.Application", pythoncom.CoInitialize())

    def get_application():
        try:
            ol = client.gencache.EnsureDispatch(
                "Outlook.Application", pythoncom.CoInitialize()
            )
            return ol
        except AttributeError:
            # Corner case dependencies.
            import os
            import re
            import sys
            import shutil

            # Remove cache and try again.
            MODULE_LIST = [m.__name__ for m in sys.modules.values()]
            for module in MODULE_LIST:
                if re.match(r"win32com\.gen_py\..+", module):
                    del sys.modules[module]
            shutil.rmtree(
                os.path.join(os.environ.get("LOCALAPPDATA"), "Temp", "gen_py")
            )

            ol = client.gencache.EnsureDispatch(
                "Outlook.Application", pythoncom.CoInitialize()
            )
            return ol

    def find_pst_folder(mapi, pst_filepath):
        dispatch = client.gencache.EnsureDispatch
        for store in dispatch(mapi.Stores):
            if store.IsDataFileStore and store.FilePath == pst_filepath:
                return store.GetRootFolder()

    def get_pst_folder(pst_filepath):
        """Returns the PST archive folder, if it doesn't exist it creates it"""
        # get pst folder
        pst_folder = find_pst_folder(outlook, pst_filepath)

        # if not found
        if not pst_folder:
            outlook.AddStoreEx(pst_filepath, const.olStoreDefault)
            pst_folder = find_pst_folder(outlook, pst_filepath)
            # add archive folder
            pst_folder.Folders.Add("Archive")
            # set the account name
            path_list = str.split(pst_filepath, "\\")
            display_name = path_list[len(path_list) - 1].replace(".pst", "")
            pst_folder.Name = display_name
        if not pst_folder:
            raise RuntimeError("Can't find PST folder at %s" % pst_filepath)

        return pst_folder

    def get_or_post(param):
        if request.GET.get(param):
            return request.GET.get(param)
        elif request.POST.get(param):
            return request.POST.get(param)
        else:
            return None

    application = get_application()
    outlook = application.GetNamespace("MAPI")
    const = client.constants
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
            emails = broadcast_instance.create_emails()
            # response = HttpResponse(
            #     content_type='file',
            #     # headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
            # )
            # response['Content-Disposition'] = 'attachment; filename="somefilename.pst"'

            pst_folder = get_pst_folder(PST_FILEPATH)

            # writer = csv.writer(response, delimiter=',', doublequote=True)
            # file_header = ["For","Subject","Body"]
            # writer.writerow(file_header)
            print("emails\n", emails)
            for email in emails:
                # writer.writerow(email)
                pst_message = pst_folder.Items.Add()
                if "subject" in email:
                    pst_message.Subject = email["subject"]
                if "email" in email:
                    pst_message.To = email["email"]
                if "body" in email:
                    pst_message.HTMLBody = email["body"]
                # pst_message.Move(pst_folder)
                pst_message.Save()
                pst_message.Close(0)
            print("pst_message", dir(pst_message))
            print("pst_folder", dir(pst_folder))
            # print(pst_folder.GetTable('Archive'))
            data = gzip.GzipFile(PST_FILEPATH, "r")
            print("application", dir(application))
            print("outlook", dir(outlook))
            # outlook.Application.Quit()
            print(data)
            # response = HttpResponse('',
            #     content_type='application/zip')
            # response['Content-Disposition'] = 'attachment; filename="somefilename.gzip"'

            # return response

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


def success(request, broadcast=""):
    broadcast = MassMail.objects.get(id=broadcast) if broadcast else None
    return render(request, "mailsender/success.html", {"broadcast": broadcast})


@login_required
def history(request):
    broadcasts = MassMail.objects.all()
    return render(request, "mailsender/history.html", {"broadcasts": broadcasts})
