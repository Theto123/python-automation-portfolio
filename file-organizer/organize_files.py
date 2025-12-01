import os
import shutil
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

EXTENSION_MAP = {
    "Images": ["jpg", "jpeg", "png", "gif", "bmp", "tiff"],
    "Documents": ["pdf", "docx", "doc", "txt", "xlsx", "pptx", "csv"],
    "Audio": ["mp3", "wav", "aac", "flac"],
    "Video": ["mp4", "avi", "mov", "mkv"],
    "Archives": ["zip", "rar", "7z", "tar", "gz"]
}

def get_category(extension):
    """Return folder category for a given file extension"""
    extension = extension.lower()
    for category, exts in EXTENSION_MAP.items():
        if extension in exts:
            return category
    return "Others"

def organize_folder(folder, dry_run=False):
    """Organize files in a folder by type, optionally recursively"""
    report = {"moved": 0, "skipped": 0, "errors": 0}

    for root, dirs, files in os.walk(folder):
        for file in files:
            try:
                path = os.path.join(root, file)
                ext = file.split(".")[-1]
                category = get_category(ext)
                target_folder = os.path.join(folder, category)
                os.makedirs(target_folder, exist_ok=True)
                target_path = os.path.join(target_folder, file)

                counter = 1
                while os.path.exists(target_path):
                    base, extension = os.path.splitext(file)
                    target_path = os.path.join(target_folder, f"{base}_{counter}{extension}")
                    counter += 1

                if not dry_run:
                    shutil.move(path, target_path)
                logging.info(f"Moved '{file}' to '{target_folder}'")
                report["moved"] += 1
            except Exception as e:
                logging.error(f"Error moving '{file}': {e}")
                report["errors"] += 1
    logging.info(f"Summary: {report}")
    return report

if __name__ == "__main__":
    folder_to_organize = "test_folder"
    organize_folder(folder_to_organize, dry_run=False)
