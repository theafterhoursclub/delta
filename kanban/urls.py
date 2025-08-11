"""urls for the kanban app"""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("backlog/", views.backlog, name="backlog"),
    path("backlog/create/", views.create_task, name="create_task"),
    path("backlog/<int:pk>/edit/", views.edit_task, name="edit_task"),
    path("kanban/", views.kanban_board, name="kanban_board"),
    path("story_board/", views.story_board, name="story_board"),
    path("kanban/reorder/", views.reorder_tasks, name="reorder_tasks"),
    path(
        "kanban/reorder_list_tasks/",
        views.reorder_list_tasks,
        name="reorder_list_tasks",
    ),
]
