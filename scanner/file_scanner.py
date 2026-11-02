
import os
from pathlib import Path
from datetime import datetime

SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx", ".doc",
    ".txt", ".md",
    ".pptx", ".ppt",
    ".xlsx", ".xls", ".csv",
    ".pages", ".numbers", ".key",
}

EXCLUDED_DIRECTORIES = {
    ".Trash",
    ".git",
    "node_modules",
    "__pycache__",
    ".cache",
    ".venv",
    "venv",
    "Caches",
    "Application Support",
    "Library",
    "personal-document-search"
}

def scan_documents(root_directory: Path) -> list[dict]:
    documents = []
    directories = [root_directory]

    while directories:
        current_directory = directories.pop()

        try:
            with os.scandir(current_directory) as entries:
                for entry in entries:
                    if entry.name.startswith("."):
                        continue
                    
                    try:
                        # Do not follow symbolic links.
                        if entry.is_symlink():
                            continue

                        if entry.is_dir(follow_symlinks=False):
                            # Skip hidden and excluded directories.
                            if entry.name.startswith("."):
                                continue

                            if entry.name in EXCLUDED_DIRECTORIES:
                                continue

                            directories.append(Path(entry.path))

                        elif entry.is_file(follow_symlinks=False):
                            path = Path(entry.path)

                            if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                                continue

                            stat = entry.stat(follow_symlinks=False)

                            documents.append({
                                "filename": path.name,
                                "extension": path.suffix.lower(),
                                "file_path": str(path),
                                "parent_folder": str(path.parent),
                                "file_size_bytes": stat.st_size,
                                "modified_at": datetime.fromtimestamp(
                                    stat.st_mtime
                                ).isoformat(timespec="seconds"),
                            })

                    except (PermissionError, OSError) as error:
                        print(f"Skipped {entry.path}: {error}")

        except (PermissionError, OSError) as error:
            print(f"Cannot access {current_directory}: {error}")

    return documents
