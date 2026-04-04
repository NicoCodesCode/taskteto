# taskteto

A simple task tracker CLI app built with argparse that writes your tasks to a JSON file.

Project made for: https://roadmap.sh/projects/task-tracker

---

## Requirements

- Python 3.10+

## Installation

Clone the repository and install it locally in editable mode:

```bash
git clone https://github.com/yourusername/taskteto.git
cd taskteto
pip install -e .
```

After installing, the `taskteto` command will be available anywhere in your terminal.

---

## Usage

### Add a task

```bash
taskteto add "buy milk"
```

### List all tasks

```bash
taskteto list
```

### List tasks by status

```bash
taskteto list --done
taskteto list --in-progress
taskteto list --todo
```

### Update a task name

```bash
taskteto update <id> "new task name"
```

### Mark a task status

```bash
taskteto mark <id> done
taskteto mark <id> in-progress
taskteto mark <id> todo
```

### Delete a task

```bash
taskteto delete <id>
```

### Help

```bash
taskteto --help
taskteto <command> --help
```
