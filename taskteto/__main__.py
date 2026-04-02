import argparse
import json

TASK_FILE = "tasklist.json"


def main():
    tasklist = load_tasks()

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(title="Actions", dest="action")

    add_parser = subparsers.add_parser("add", help="add a new task")
    add_parser.add_argument("task", help="the name of the task to add")

    args = parser.parse_args()

    if args.action == "add":
        add_task(args.task, tasklist)
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


def add_task(task, tasklist):
    tasklist.append(task)
    if write_tasks(tasklist):
        print(f"'{task}' was added to the list")


if __name__ == "__main__":
    main()
