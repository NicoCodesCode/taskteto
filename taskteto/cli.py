import argparse
from taskteto.storage import load_tasks
from taskteto.tasks import *


def main():
    tasklist = load_tasks()

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
        add_task(args.task_name, tasklist)
    elif args.action == "list":
        if args.done:
            list_tasks_by_status(tasklist, TaskStatus.DONE.value)
        elif args.in_progress:
            list_tasks_by_status(tasklist, TaskStatus.IN_PROGRESS.value)
        elif args.todo:
            list_tasks_by_status(tasklist, TaskStatus.TODO.value)
        else:
            list_tasks(tasklist)
    elif args.action == "update":
        update_task(args.task_id, args.new_task_name, tasklist)
    elif args.action == "mark":
        mark_task_status(args.task_id, args.task_status, tasklist)
    elif args.action == "delete":
        delete_task(args.task_id, tasklist)
    else:
        parser.print_help()
