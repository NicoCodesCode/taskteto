import argparse
import json
from enum import Enum

TASK_FILE = "tasklist.json"


class TaskStatus(Enum):
    DONE = "done"
    IN_PROGRESS = "in-progress"
    TODO = "todo"


def main():
    tasks = load_tasks()

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(title="Actions", dest="action")

    add_parser = subparsers.add_parser("add", help="add a new task")
    add_parser.add_argument("task_name", help="the name of the task to add")

    list_parser = subparsers.add_parser("list", help="list all tasks")
    list_parser.add_argument(
        "-d", "--done", action="store_true", help="list all done tasks"
    )
    list_parser.add_argument(
        "-p",
        "--in-progress",
        action="store_true",
        help="list all in-progress tasks",
    )
    list_parser.add_argument(
        "-t", "--todo", action="store_true", help="list all todo tasks"
    )

    update_parser = subparsers.add_parser(
        "update", help="update the name of a task by ID"
    )
    update_parser.add_argument("task_id", type=int, help="the task ID")
    update_parser.add_argument("new_task_name", help="the new name for the task")

    mark_parser = subparsers.add_parser("mark", help="mark the task status")
    mark_parser.add_argument(
        "task_status",
        choices=[s.value for s in TaskStatus],
        help="the status to assign",
    )
    mark_parser.add_argument("task_id", type=int, help="the task ID")

    delete_parser = subparsers.add_parser("delete", help="delete a task by ID")
    delete_parser.add_argument("task_id", type=int, help="the task ID")

    args = parser.parse_args()

    if args.action == "add":
        add_task(args.task_name, tasks)
    elif args.action == "list":
        if args.done:
            list_done_tasks(tasks)
        elif args.in_progress:
            list_in_progress_tasks(tasks)
        elif args.todo:
            list_todo_tasks(tasks)
        else:
            list_tasks(tasks)
    elif args.action == "update":
        update_task(args.task_id, args.new_task_name, tasks)
    elif args.action == "mark":
        mark_task_status(args.task_id, args.task_status, tasks)
    elif args.action == "delete":
        delete_task(args.task_id, tasks)
    else:
        parser.print_help()


def load_tasks():
    try:
        with open(TASK_FILE, mode="r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def write_tasks(tasks):
    try:
        with open(TASK_FILE, mode="w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=4)
        return True
    except OSError as e:
        print(f"Error saving tasks: {e}")
        return False


def find_task_index(task_id, tasks):
    return next((i for i, task in enumerate(tasks) if task["id"] == task_id), None)


def add_task(task_name, tasks):
    task_id = max((task["id"] for task in tasks), default=0) + 1
    new_task = {"id": task_id, "task_name": task_name, "status": TaskStatus.TODO.value}
    tasks.append(new_task)

    if write_tasks(tasks):
        print(f"'{task_name}' was added to the list (ID: {task_id})")


def list_tasks(tasks):
    if len(tasks) > 0:
        for task in tasks:
            print(f"(ID: {task["id"]}) {task["task_name"]} -- {task["status"]}")
    else:
        print("There are no tasks ^^")


def list_done_tasks(tasks):
    done_tasks = [t for t in tasks if t["status"] == TaskStatus.DONE.value]
    list_tasks(done_tasks)


def list_in_progress_tasks(tasks):
    in_progress_tasks = [
        t for t in tasks if t["status"] == TaskStatus.IN_PROGRESS.value
    ]
    list_tasks(in_progress_tasks)


def list_todo_tasks(tasks):
    todo_tasks = [t for t in tasks if t["status"] == TaskStatus.TODO.value]
    list_tasks(todo_tasks)


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


if __name__ == "__main__":
    main()
