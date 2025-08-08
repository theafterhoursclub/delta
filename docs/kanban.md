# Kanban Module

The `kanban` Django app provides the core functionality for project and task management.

## Models

::: kanban.models.Task

## Views

- `kanban_board`: Displays the Kanban board with columns for each status.
- `task_list`: Shows all tasks in a table.
- `create_task`: Form to create a new task.
- `edit_task`: Edit an existing task.
- `reorder_tasks`: Handles AJAX requests to update task order and status.

## Templates

- `kanban_board.html`: Kanban board UI.
- `task_list.html`: Task list table.
- `create_task.html`: Task creation form.
- `edit_task.html`: Task editing form.
- `sidebar.html`: Navigation sidebar.

## Static

- `colors.css`: Color scheme.
- JS/CSS for AG Grid, Bootstrap, SortableJS.


