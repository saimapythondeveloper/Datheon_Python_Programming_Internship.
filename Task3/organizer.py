import os
import shutil
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

# File extension mapping
FILE_TYPES = {
    # Documents
    ".pdf": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",
    ".ppt": "Documents",
    ".pptx": "Documents",
    ".xls": "Documents",
    ".xlsx": "Documents",
    ".csv": "Documents",

    # Images
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".bmp": "Images",
    ".webp": "Images",

    # Videos
    ".mp4": "Videos",
    ".mkv": "Videos",
    ".mov": "Videos",
    ".avi": "Videos",

    # Archives
    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
    ".tar": "Archives",
    ".gz": "Archives",

    # Code
    ".py": "Code",
    ".java": "Code",
    ".cpp": "Code",
    ".c": "Code",
    ".html": "Code",
    ".css": "Code",
    ".js": "Code",
    ".dart": "Code",
    ".json": "Code"
}


def get_unique_path(destination):
    """Generate a new filename if the destination already exists."""
    if not destination.exists():
        return destination

    folder = destination.parent
    name = destination.stem
    extension = destination.suffix
    counter = 1

    while True:
        new_path = folder / f"{name}_{counter}{extension}"

        if not new_path.exists():
            return new_path

        counter += 1


def organize_files(folder_path):
    folder = Path(folder_path).expanduser()

    if not folder.exists() or not folder.is_dir():
        logging.error("The specified directory does not exist.")
        return

    moved = 0
    skipped = 0
    failed = 0

    # Scan the selected directory
    try:
        with os.scandir(folder) as entries:
            for entry in entries:
                if not entry.is_file(follow_symlinks=False):
                    continue

                source = Path(entry.path)

                # Do not move the currently running script
                if source.resolve() == Path(__file__).resolve():
                    skipped += 1
                    continue

                # Identify the file category
                category = FILE_TYPES.get(source.suffix.lower())

                # Skip unknown extensions
                if category is None:
                    skipped += 1
                    logging.info(f"Skipped: {source.name}")
                    continue

                destination_folder = folder / category
                destination = destination_folder / source.name

                try:
                    # Create category folder if necessary
                    destination_folder.mkdir(exist_ok=True)

                    # Prevent overwriting duplicate filenames
                    destination = get_unique_path(destination)

                    # Move the file
                    shutil.move(str(source), str(destination))

                    moved += 1
                    logging.info(
                        f"Moved: {source.name} -> {category}/"
                        f"{destination.name}"
                    )

                except (PermissionError, FileExistsError) as error:
                    failed += 1
                    logging.error(
                        f"Could not move {source.name}: {error}"
                    )

                except OSError as error:
                    failed += 1
                    logging.error(
                        f"File operation failed for "
                        f"{source.name}: {error}"
                    )

    except (PermissionError, OSError) as error:
        logging.error(f"Cannot scan the directory: {error}")
        return

    # Execution summary
    print("\n" + "=" * 35)
    print("     FILE ORGANIZER SUMMARY")
    print("=" * 35)
    print(f"Files moved successfully : {moved}")
    print(f"Files skipped            : {skipped}")
    print(f"Files failed             : {failed}")
    print("=" * 35)


if __name__ == "__main__":
    path = input(
        "Enter folder path (press Enter for Downloads): "
    ).strip().strip('"')

    if not path:
        path = Path.home() / "Downloads"

    organize_files(path)
