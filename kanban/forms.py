"""Forms for the kanban app."""

from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    """Form for creating and updating Task instances."""

    class Meta:  # pylint: disable=too-few-public-methods, disable=missing-class-docstring
        model = Task
        fields = [
            "title",
            "description",
            "status",
            "task_type",
            "due_date",
            "bau_working_day",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "id": "id_description"}
            ),
            "status": forms.Select(attrs={"class": "form-control"}),
            "task_type": forms.Select(attrs={"class": "form-control"}),
            "due_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "bau_working_day": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove hiding from the field widgets themselves
        self.fields["due_date"].widget.attrs.pop("style", None)
        self.fields["bau_working_day"].widget.attrs.pop("style", None)

        # Determine task_type from form data or instance
        task_type = (
            self.data.get("task_type")
            or getattr(self.instance, "task_type", None)
            or "task"
        )
        if isinstance(task_type, str) and task_type.lower() == "bau":
            self.fields["bau_working_day"].widget.attrs["style"] = ""
        elif isinstance(task_type, str):
            self.fields["due_date"].widget.attrs["style"] = ""
