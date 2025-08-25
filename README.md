# Delta

Delta is a Django-based web application designed to support easier project and task management. It provides a simple interface for creating, organizing, and tracking tasks, including a Kanban board for visual workflow management.

## Features

- Create, edit, and manage tasks with details such as title, description, status, and due date.
- Visual Kanban board with columns for each workflow status (To Do, In Progress, Help, Done).
- Drag-and-drop task reordering and status changes.
- Bootstrap-powered responsive UI for a modern user experience.

## Purpose

The purpose of this package is to streamline project and task management, making it easier for individuals and teams to organize their work, track progress, and collaborate effectively.

## Getting Started

1. Install dependencies from `pyproject.toml`.
2. Run migrations to set up the database.
```powershell
python manage.py makemigrations
python manage.py migrate
```
3. Start the Django development server.
```powershell
python manage.py runserver
```
4. Access the application in your browser to begin managing your projects and tasks.

---

