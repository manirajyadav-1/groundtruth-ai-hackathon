import os
import shutil
import uuid
from fastapi import UploadFile
from app.config import settings

async def save_upload_file(upload_file: UploadFile) -> str:
    """Saves an uploaded file to the temp directory and returns the file path."""
    file_ext = os.path.splitext(upload_file.filename)[1]
    filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(settings.TEMP_DIR, filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
        
    return file_path

def create_zip_archive(source_dir: str, output_filename: str) -> str:
    """Creates a ZIP archive of the source directory."""
    zip_path = os.path.join(settings.OUTPUT_DIR, output_filename)
    shutil.make_archive(zip_path.replace(".zip", ""), 'zip', source_dir)
    return zip_path

def cleanup_temp_files(file_paths: list[str]):
    """Removes temporary files."""
    for path in file_paths:
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception as e:
            print(f"Error deleting {path}: {e}")
