from django.shortcuts import redirect


def home(_request):
    return redirect("agendas:home")

def password_updated(_request):
    return redirect("accounts:password_updated")
