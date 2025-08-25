from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("create-organisation/", views.create_organisation, name="create_organisation"),
    path("create-team/", views.create_team, name="create_team"),
]
