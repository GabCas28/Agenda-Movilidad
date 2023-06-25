from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from .forms import AccountForm


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            else:
                return redirect("agendas:home")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})


def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect("agendas:home")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(
                "accounts:login"
            )  # Redirect to the login page after successful registration
    else:
        form = AccountForm()
    return render(request, "accounts/register.html", {"form": form})


def staff_only(request):
    return render(request, "accounts/staff_only.html")
