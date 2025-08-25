from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Organisation, Team, CustomUser
from django import forms

# --- Forms ---


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")


class OrganisationForm(forms.ModelForm):
    class Meta:
        model = Organisation
        fields = ("name",)


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ("name", "organisation")


# --- Views ---


def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("create_organisation")
    else:
        form = CustomUserCreationForm()
    return render(request, "users/signup.html", {"form": form})


def create_organisation(request):
    if request.method == "POST":
        form = OrganisationForm(request.POST)
        if form.is_valid():
            organisation = form.save()
            # Optionally link the user to the organisation here
            request.user.organisation = organisation
            request.user.save()
            return redirect("create_team")
    else:
        form = OrganisationForm()
    return render(request, "users/create_organisation.html", {"form": form})


def create_team(request):
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save()
            # Optionally link the user to the team here
            request.user.team = team
            request.user.save()
            return redirect("home")  # or wherever you want to send them next
    else:
        form = TeamForm()
    return render(request, "users/create_team.html", {"form": form})
