from flask import Flask
from flask_cors import CORS
import os

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    from app.config import config
    app.config.from_object(config[config_name])
    
    # Initialize CORS
    CORS(app)
    
    # Create necessary directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
    
    # Register blueprints
    from app.routes.upload_routes import upload_bp
    from app.routes.analysis_routes import analysis_bp
    from app.routes.download_routes import download_bp
    
    app.register_blueprint(upload_bp, url_prefix='/api/upload')
    app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
    app.register_blueprint(download_bp, url_prefix='/api/download')
    
    # Health check endpoint
    @app.route('/api/health')
    def health():
        return {'status': 'healthy', 'message': 'Database Normalization API is running'}
    
    return app
