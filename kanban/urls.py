from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("tasks/", views.task_list, name="task_list"),
    path("tasks/create/", views.create_task, name="create_task"),
    path("tasks/<int:pk>/edit/", views.edit_task, name="edit_task"),
    path("kanban/", views.kanban_board, name="kanban_board"),
    path("kanban/reorder/", views.reorder_tasks, name="reorder_tasks"),
]
