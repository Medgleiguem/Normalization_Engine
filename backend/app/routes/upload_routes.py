"""
Upload routes - handle file uploads
"""
from flask import Blueprint, request, jsonify
from app.utils.file_handler import save_uploaded_file, allowed_file

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/', methods=['POST'])
def upload_file():
    """Handle Excel file upload"""
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only .xlsx and .xls files are allowed.'}), 400
        
        # Save file
        file_path, file_id = save_uploaded_file(file)
        
        return jsonify({
            'success': True,
            'file_id': file_id,
            'filename': file.filename,
            'message': 'File uploaded successfully'
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
