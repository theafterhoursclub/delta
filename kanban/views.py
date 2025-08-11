"""Views for the Kanban application."""

# pylint: disable=no-member
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Task
from .forms import TaskForm


def home(request):
    """Render the home page."""
    return render(request, "kanban/home.html")


def backlog(request):
    """Render the task list, ordered by list_order."""
    tasks = Task.list_ordered()
    return render(request, "kanban/backlog.html", {"tasks": tasks})


def create_task(request):
    """Create a new task."""
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("backlog")
    else:
        form = TaskForm()
    return render(request, "kanban/create_task.html", {"form": form})


def kanban_board(request):
    """Render the Kanban board, grouping tasks by status and ordering by 'order'."""
    statuses = ["todo", "in_progress", "help", "done"]
    tasks_by_status = {status: [] for status in statuses}
    for task in Task.objects.exclude(task_type="story").order_by("order"):
        if task.status in tasks_by_status:
            tasks_by_status[task.status].append(task)
    return render(
        request,
        "kanban/kanban_board.html",
        {
            "tasks_by_status": tasks_by_status,
            "statuses": statuses,
            "task_type": "All Tasks",
        },
    )


def story_board(request):
    """Render the story board, grouping tasks by status and ordering by 'order'."""
    statuses = ["todo", "in_progress", "help", "done"]
    tasks_by_status = {status: [] for status in statuses}
    for task in Task.objects.filter(task_type="story").order_by("order"):
        if task.status in tasks_by_status:
            tasks_by_status[task.status].append(task)
    return render(
        request,
        "kanban/kanban_board.html",
        {
            "tasks_by_status": tasks_by_status,
            "statuses": statuses,
            "task_type": "All Stories",
        },
    )


def edit_task(request, pk):
    """Edit an existing task."""
    task = Task.objects.get(pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("backlog")
    else:
        form = TaskForm(instance=task)
    return render(request, "kanban/edit_task.html", {"form": form, "task": task})


def reorder_tasks(request):
    """Reorder tasks by 'order' and update their status."""
    if request.method == "POST":
        data = json.loads(request.body)
        status = data.get("status")
        ordered_ids = data.get("ordered_ids", [])

        # Update the order and status for each task in the new order
        for idx, task_id in enumerate(ordered_ids):
            Task.objects.filter(id=task_id).update(order=idx, status=status)

        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)


def reorder_list_tasks(request):
    """Reorder tasks by 'list_order'."""
    if request.method == "POST":
        data = json.loads(request.body)
        ordered_ids = data.get("ordered_ids", [])

        # Update the list_order for each task in the new order
        for idx, task_id in enumerate(ordered_ids):
            Task.objects.filter(id=task_id).update(list_order=idx)

        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)
