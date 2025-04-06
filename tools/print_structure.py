import os

# Папки, которые не нужно отображать
EXCLUDE_DIRS = {'.venv', '.idea', '__pycache__', '.git', '.mypy_cache'}


def print_tree(start_path: str, prefix: str = ""):
    items = sorted(
        [item for item in os.listdir(start_path) if item not in EXCLUDE_DIRS]
    )
    for index, item in enumerate(items):
        path = os.path.join(start_path, item)
        is_last = index == len(items) - 1
        branch = "└── " if is_last else "├── "
        print(prefix + branch + item)
        if os.path.isdir(path):
            extension = "    " if is_last else "│   "
            print_tree(path, prefix + extension)


if __name__ == "__main__":
    print("Project Structure:\n")
    print_tree(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
