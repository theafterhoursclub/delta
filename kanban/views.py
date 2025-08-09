from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm
from collections import defaultdict
from django.http import JsonResponse
import json


def home(request):
    return render(request, "kanban/home.html")


def task_list(request):
    tasks = Task.objects.all()
    return render(request, "kanban/task_list.html", {"tasks": tasks})


def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "kanban/create_task.html", {"form": form})


def kanban_board(request):
    statuses = ["todo", "in_progress", "help", "done"]
    tasks_by_status = {status: [] for status in statuses}
    for task in Task.objects.all():
        if task.status in tasks_by_status:
            tasks_by_status[task.status].append(task)
    return render(
        request,
        "kanban/kanban_board.html",
        {
            "tasks_by_status": tasks_by_status,
            "statuses": statuses,
        },
    )


def edit_task(request, pk):
    task = Task.objects.get(pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)
    return render(request, "kanban/edit_task.html", {"form": form, "task": task})


def reorder_tasks(request):
    if request.method == "POST":
        data = json.loads(request.body)
        status = data.get("status")
        ordered_ids = data.get("ordered_ids", [])

        # Update the order and status for each task in the new order
        for idx, task_id in enumerate(ordered_ids):
            Task.objects.filter(id=task_id).update(order=idx, status=status)

        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)
