import argparse
import json
from dataclasses import dataclass, asdict


@dataclass
class Task:
    id: int
    task: str


TASK_FILE = "tasklist.json"


def main():
    tasks = load_tasks()

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(title="Actions", dest="action")

    add_parser = subparsers.add_parser("add", help="add a new task")
    add_parser.add_argument("taskname", help="the name of the task to add")

    args = parser.parse_args()

    if args.action == "add":
        add_task(args.taskname, tasks)
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


def add_task(taskname, tasks):
    task_id = max((task["id"] for task in tasks), default=0) + 1
    new_task = Task(task_id, taskname)
    tasks.append(asdict(new_task))

    if write_tasks(tasks):
        print(f"'{taskname}' was added to the list")


if __name__ == "__main__":
    main()
