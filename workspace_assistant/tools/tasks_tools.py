"""
Option B: Tasks Manager Tools

Implements tools for managing Google Tasks: listing, creating, completing,
updating, and deleting tasks. Each tool authenticates via get_tasks_service()
and returns a dict with a 'status' key ('success' or 'error').
"""

from typing import Optional
from tools.auth import get_tasks_service
 
DEFAULT_TASKLIST = "@default"

 
def list_tasks(tasklist_id: str = DEFAULT_TASKLIST, show_completed: bool = False, max_results: int = 20) -> dict:
    """List tasks from a Google Tasks list.

    Args:
        tasklist_id: ID of the task list to read from. Defaults to the
            user's default task list ("@default").
        show_completed: Whether to include tasks already marked complete.
        max_results: Maximum number of tasks to return.

    Returns:
        dict with 'status' and 'tasks' (list of task dicts) on success,
        or 'status' and 'message' on error.
    """
    try:
        service = get_tasks_service()
        result = service.tasks().list(
            tasklist=tasklist_id,
            showCompleted=show_completed,
            maxResults=max_results,
        ).execute()
        items = result.get("items", [])
        tasks = [
            {
                "id": t.get("id"),
                "title": t.get("title"),
                "notes": t.get("notes"),
                "due": t.get("due"),
                "status": t.get("status"),
            }
            for t in items
        ]
        return {"status": "success", "tasks": tasks, "count": len(tasks)}
    except Exception as e:
        return {"status": "error", "message": f"Could not list tasks: {str(e)}"}


def create_task(title: str, notes: Optional[str] = None, due: Optional[str] = None, tasklist_id: str = DEFAULT_TASKLIST) -> dict:
    """Create a new task in a Google Tasks list.

    Args:
        title: The title of the task. Required.
        notes: Optional additional details about the task.
        due: Optional due date/time in RFC 3339 format (e.g. "2026-07-15T00:00:00.000Z").
        tasklist_id: ID of the task list to add the task to. Defaults to "@default".

    Returns:
        dict with 'status' and the created 'task' on success,
        or 'status' and 'message' on error.
    """
    try:
        if not title or not title.strip():
            return {"status": "error", "message": "Task title cannot be empty."}

        service = get_tasks_service()
        body = {"title": title}
        if notes:
            body["notes"] = notes
        if due:
            body["due"] = due

        created = service.tasks().insert(tasklist=tasklist_id, body=body).execute()
        return {
            "status": "success",
            "task": {
                "id": created.get("id"),
                "title": created.get("title"),
                "notes": created.get("notes"),
                "due": created.get("due"),
            },
        }
    except Exception as e:
        return {"status": "error", "message": f"Could not create task: {str(e)}"}


def complete_task(task_id: str, tasklist_id: str = DEFAULT_TASKLIST) -> dict:
    """Mark a task as completed.

    Args:
        task_id: ID of the task to mark complete.
        tasklist_id: ID of the task list the task belongs to. Defaults to "@default".

    Returns:
        dict with 'status' and the updated 'task' on success,
        or 'status' and 'message' on error.
    """
    try:
        service = get_tasks_service()
        updated = service.tasks().patch(
            tasklist=tasklist_id,
            task=task_id,
            body={"status": "completed"},
        ).execute()
        return {
            "status": "success",
            "task": {"id": updated.get("id"), "title": updated.get("title"), "status": updated.get("status")},
        }
    except Exception as e:
        return {"status": "error", "message": f"Could not complete task {task_id}: {str(e)}"}


def update_task(task_id: str, title: Optional[str] = None, notes: Optional[str] = None, due: Optional[str] = None, tasklist_id: str = DEFAULT_TASKLIST) -> dict:
    """Update details of an existing task.

    Args:
        task_id: ID of the task to update. Required.
        title: New title for the task, if changing it.
        notes: New notes for the task, if changing them.
        due: New due date/time in RFC 3339 format, if changing it.
        tasklist_id: ID of the task list the task belongs to. Defaults to "@default".

    Returns:
        dict with 'status' and the updated 'task' on success,
        or 'status' and 'message' on error.
    """
    try:
        if not any([title, notes, due]):
            return {"status": "error", "message": "Provide at least one field to update (title, notes, or due)."}

        service = get_tasks_service()
        body = {}
        if title:
            body["title"] = title
        if notes:
            body["notes"] = notes
        if due:
            body["due"] = due

        updated = service.tasks().patch(tasklist=tasklist_id, task=task_id, body=body).execute()
        return {
            "status": "success",
            "task": {
                "id": updated.get("id"),
                "title": updated.get("title"),
                "notes": updated.get("notes"),
                "due": updated.get("due"),
            },
        }
    except Exception as e:
        return {"status": "error", "message": f"Could not update task {task_id}: {str(e)}"}


def delete_task(task_id: str, tasklist_id: str = DEFAULT_TASKLIST) -> dict:
    """Permanently delete a task from a task list.

    Args:
        task_id: ID of the task to delete. Required.
        tasklist_id: ID of the task list the task belongs to. Defaults to "@default".

    Returns:
        dict with 'status' set to 'success' and the deleted task id,
        or 'status' and 'message' on error.
    """
    try:
        service = get_tasks_service()
        service.tasks().delete(tasklist=tasklist_id, task=task_id).execute()
        return {"status": "success", "deleted_task_id": task_id}
    except Exception as e:
        return {"status": "error", "message": f"Could not delete task {task_id}: {str(e)}"}


tasks_tools = [
    list_tasks,
    create_task,
    complete_task,
    update_task,
    delete_task,
]