from enum import Enum
from taskteto.storage import write_tasks


class TaskStatus(Enum):
    DONE = "done"
    IN_PROGRESS = "in-progress"
    TODO = "todo"


def find_task_index(task_id, tasks):
    return next((i for i, task in enumerate(tasks) if task["id"] == task_id), None)


def add_task(task_name, tasks):
    task_id = max((task["id"] for task in tasks), default=0) + 1
    new_task = {"id": task_id, "task_name": task_name, "status": TaskStatus.TODO.value}
    tasks.append(new_task)

    if write_tasks(tasks):
        print(f"'{task_name}' was added to the list (ID: {task_id})")


def list_tasks(tasks):
    for task in tasks:
        print(f"(ID: {task["id"]}) {task["task_name"]} -- {task["status"]}")


def list_tasks_by_status(tasks, status):
    filtered_tasks = [t for t in tasks if t["status"] == status]
    list_tasks(filtered_tasks)


def update_task(task_id, new_task_name, tasks):
    task_index = find_task_index(task_id, tasks)

    if task_index is not None:
        tasks[task_index]["task_name"] = new_task_name
        if write_tasks(tasks):
            print(f"Task {task_id} was updated to '{new_task_name}'")
    else:
        print(f"Couldn't find task with ID: {task_id}")


def mark_task_status(task_id, status, tasks):
    task_index = find_task_index(task_id, tasks)

    if task_index is not None:
        tasks[task_index]["status"] = status
        if write_tasks(tasks):
            print(f"'{tasks[task_index]["task_name"]}' was marked as {status}")
    else:
        print(f"Couldn't find task with ID: {task_id}")


def delete_task(task_id, tasks):
    task_index = find_task_index(task_id, tasks)

    if task_index is not None:
        task_name = tasks.pop(task_index)["task_name"]
        if write_tasks(tasks):
            print(f"'{task_name}' was removed from the list")
    else:
        print(f"Couldn't find task with ID: {task_id}")
