import os
from fastapi import HTTPException, UploadFile

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "mp4"}
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "video/mp4"}

def validate_file(file: UploadFile) -> None:
    # Check extension
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"File extension not allowed: {ext}")
    
    # Check mime type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail=f"File content type not allowed: {file.content_type}")

def sanitize_filename(filename: str) -> str:
    import re
    # simple replace
    s = re.sub(r"[^\w\.-]", "_", filename)
    return s
