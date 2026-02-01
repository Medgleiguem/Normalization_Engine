"""
File validation and handling utilities
"""
import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_uploaded_file(file) -> tuple[str, str]:
    """
    Save uploaded file and return (file_path, file_id)
    """
    if not file or not allowed_file(file.filename):
        raise ValueError("Invalid file type. Only .xlsx and .xls files are allowed.")
    
    # Generate unique file ID
    file_id = str(uuid.uuid4())
    
    # Secure filename
    filename = secure_filename(file.filename)
    original_name, ext = os.path.splitext(filename)
    
    # Create unique filename
    unique_filename = f"{file_id}_{filename}"
    
    # Save file
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(file_path)
    
    return file_path, file_id

def cleanup_file(file_path: str):
    """Delete a file if it exists"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        current_app.logger.error(f"Error deleting file {file_path}: {e}")

def get_output_path(file_id: str, suffix: str, extension: str) -> str:
    """Generate output file path"""
    filename = f"{file_id}_{suffix}.{extension}"
    return os.path.join(current_app.config['OUTPUT_FOLDER'], filename)
