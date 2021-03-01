from django.shortcuts import render, redirect
from .models import Broadcast
from .forms import BroadcastForm
from django.core.exceptions import ValidationError

def form(request, broadcast=""):
    broadcast = Broadcast.objects.get(id=broadcast) if broadcast else None
    if request.method == "POST":
        form = BroadcastForm(request.POST or None, instance=broadcast)
        if form.is_valid():
            broadcast_instance=form.save()
            broadcast_instance.send(engine=chooseEngine(request.POST["user"]), user=request.POST["user"], password=request.POST["password"])
            return redirect('sender:success', broadcast_instance.id)
    else:
        form = BroadcastForm()
    return render(request, "mailsender/form.html", {"broadcast": broadcast, "form": form})

def chooseEngine(x):
    if 'gmail' in x:
        return 'gmail'
    elif 'ugr' in x:
        return 'ugr'
    else:
        raise ValidationError("Servicio de email no soportado")

def success(request, broadcast=""):
    broadcast = Broadcast.objects.get(id=broadcast) if broadcast else None
    return render(request, "mailsender/success.html", {"broadcast": broadcast})


def history(request):
    broadcasts = Broadcast.objects.all()
    return render(request, "mailsender/history.html", {"broadcasts": broadcasts})
