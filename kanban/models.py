"""Models for the Kanban application, including Task and related logic."""

# pylint: disable=no-member
import datetime  # Fix: import datetime for date handling
from django.db import models

STATUS_CHOICES = [
    ("backlog", "Backlog"),
    ("todo", "To Do"),
    ("in_progress", "In Progress"),
    ("help", "Help"),
    ("done", "Done"),
]


TASK_TYPE_CHOICES = [
    ("task", "Task"),
    ("story", "Story"),
    ("bau", "BAU"),
]


WD_CHOICES = [(f"WD{i}", f"WD{i}") for i in range(1, 32)]


class Task(models.Model):
    """This holds information about a task"""

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="backlog")
    task_type = models.CharField(
        max_length=20, choices=TASK_TYPE_CHOICES, default="task"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(
        "users.CustomUser", on_delete=models.SET_NULL, null=True, blank=True
    )
    due_date = models.DateField(blank=True, null=True)
    bau_working_day = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="For BAU tasks, e.g. WD3",
        choices=WD_CHOICES,
    )
    order = models.PositiveIntegerField(default=0)
    list_order = models.PositiveIntegerField(default=0)

    # Link to another Task, but only if it's a Story
    linked_story = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="linked_tasks",
        limit_choices_to={"task_type": "story"},
        help_text="Link this task to a Story (another Task with type 'Story').",
    )

    def __str__(self):
        # Fix: Ensure __str__ always returns a string
        return str(self.title)

    def get_due_display(self):
        """Return the appropriate due value based on task_type."""
        if self.task_type.lower() == "bau" and self.bau_working_day:
            return self.bau_working_day
        return self.due_date

    def get_due_date_for_working_day(self, year, month, bank_holidays=None):
        """
        Returns the date for the Nth working day (Monday-Friday, excluding bank holidays)
        starting from the given month and year.
        If bau_working_day exceeds the number of working days in the month, continues into the next
         month(s).
        bau_working_day is 1-based (WD1 = first working day).
        bank_holidays: optional set/list of datetime.date objects to skip as working days.
        """
        day = 1
        count = 0
        current_year = year
        current_month = month
        try:
            wd_number = int(str(self.bau_working_day).replace("WD", ""))
        except (ValueError, AttributeError):  # Fix: catch only relevant exceptions
            return None
        if bank_holidays is None:
            bank_holidays = set()
        else:
            bank_holidays = set(bank_holidays)
        while True:
            try:
                date = datetime.date(current_year, current_month, day)
            except ValueError:
                # Move to next month
                if current_month == 12:
                    current_month = 1
                    current_year += 1
                else:
                    current_month += 1
                day = 1
                continue
            if date.weekday() < 5 and date not in bank_holidays:  # 0=Monday, 4=Friday
                count += 1
                if count == wd_number:
                    return date
            day += 1

    @classmethod
    def ordered(cls):
        """Return queryset ordered by 'order'."""
        return cls.objects.order_by("order")

    @classmethod
    def list_ordered(cls):
        """Return queryset ordered by 'list_order'."""
        return cls.objects.order_by("list_order")

    def save(self, *args, **kwargs):
        if self._state.adding and not self.list_order:
            max_order = Task.objects.count()
            self.list_order = max_order + 1
        super().save(*args, **kwargs)


class Sprint(models.Model):
    """This holds information about a sprint"""

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
