"""
User Models contains everything required for a user/org/team
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class Organisation(models.Model):
    """Every team and user must be part of an organisations"""

    name = models.CharField(max_length=100)


class Team(models.Model):
    """Every team member must be part of a team, and a team must be part of an organisation"""

    name = models.CharField(max_length=100)
    team = models.ForeignKey("Organisation", on_delete=models.CASCADE)


class CustomUser(AbstractUser):
    """Custom User inherits from AbstractUser. Fields include:
    - username, first_name, last_name, email
    - is_staff or is_superuser
    """

    bio = models.TextField(blank=True, null=True)
    team = models.ForeignKey(
        Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="users"
    )
