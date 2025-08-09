"""Forms for the kanban app."""

from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    """Form for creating and updating Task instances."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Class fields/Meta"""

        model = Task
        fields = ["title", "description", "status", "due_date"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "due_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
        }
