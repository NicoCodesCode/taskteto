import argparse
import json

TASK_FILE = "tasklist.json"


def main():
    tasks = load_tasks()

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(title="Actions", dest="action")

    add_parser = subparsers.add_parser("add", help="add a new task")
    add_parser.add_argument("task_name", help="the name of the task to add")

    update_parser = subparsers.add_parser(
        "update", help="update the name of a task by ID"
    )
    update_parser.add_argument("task_id", type=int, help="the task ID")
    update_parser.add_argument("new_task_name", help="the new name for the task")

    delete_parser = subparsers.add_parser("delete", help="delete a task by ID")
    delete_parser.add_argument("task_id", type=int, help="the task ID")

    args = parser.parse_args()

    if args.action == "add":
        add_task(args.task_name, tasks)
    elif args.action == "update":
        update_task(args.task_id, args.new_task_name, tasks)
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
            json.dump(tasks, f)
        return True
    except OSError as e:
        print(f"Error saving tasks: {e}")
        return False


def find_task_index(task_id, tasks):
    return next((i for i, task in enumerate(tasks) if task["id"] == task_id), None)


def add_task(task_name, tasks):
    task_id = max((task["id"] for task in tasks), default=0) + 1
    new_task = {"id": task_id, "task_name": task_name}
    tasks.append(new_task)

    if write_tasks(tasks):
        print(f"'{task_name}' was added to the list (ID: {task_id})")


def update_task(task_id, new_task_name, tasks):
    task_index = find_task_index(task_id, tasks)

    if task_index is not None:
        tasks[task_index]["task_name"] = new_task_name
        if write_tasks(tasks):
            print(f"Task {task_id} was updated to '{new_task_name}'")
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
