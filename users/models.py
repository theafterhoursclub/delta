from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Fields inherited from AbstractUser:
    # username, first_name, last_name, email
    # is_staff or is_superuser
    bio = models.TextField(blank=True, null=True)