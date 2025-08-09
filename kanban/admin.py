from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "due_date", "created_at", "updated_at", "order")
    list_filter = ("status", "due_date")
    search_fields = ("title", "description")
    ordering = ("status", "order", "due_date")
