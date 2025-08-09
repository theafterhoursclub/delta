"""App configuration for the kanban app."""

from django.apps import AppConfig


class KanbanConfig(AppConfig):
    """Configuration for the kanban application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "kanban"
