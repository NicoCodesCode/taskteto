import json

TASK_FILE = "tasklist.json"


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
