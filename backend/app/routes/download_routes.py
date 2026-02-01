"""
Download routes - handle file downloads
"""
from flask import Blueprint, send_file, jsonify, current_app
import os

download_bp = Blueprint('download', __name__)

# Import cache from analysis routes
from app.routes.analysis_routes import analysis_cache

@download_bp.route('/report/<analysis_id>', methods=['GET'])
def download_report(analysis_id):
    """Download normalization report"""
    if analysis_id not in analysis_cache:
        return jsonify({'error': 'Analysis not found'}), 404
    
    cached = analysis_cache[analysis_id]
    report_path = cached['report_path']
    
    if not os.path.exists(report_path):
        return jsonify({'error': 'Report file not found'}), 404
    
    return send_file(
        report_path,
        as_attachment=True,
        download_name='normalization_report.docx',
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )

@download_bp.route('/sql/<analysis_id>', methods=['GET'])
def download_sql(analysis_id):
    """Download SQL script"""
    if analysis_id not in analysis_cache:
        return jsonify({'error': 'Analysis not found'}), 404
    
    cached = analysis_cache[analysis_id]
    sql_path = cached['sql_path']
    
    if not os.path.exists(sql_path):
        return jsonify({'error': 'SQL file not found'}), 404
    
    return send_file(
        sql_path,
        as_attachment=True,
        download_name='database_schema.sql',
        mimetype='application/sql'
    )

@download_bp.route('/excel/<analysis_id>', methods=['GET'])
def download_excel(analysis_id):
    """Download normalized Excel file"""
    if analysis_id not in analysis_cache:
        return jsonify({'error': 'Analysis not found'}), 404
    
    cached = analysis_cache[analysis_id]
    excel_path = cached['excel_path']
    
    if not os.path.exists(excel_path):
        return jsonify({'error': 'Excel file not found'}), 404
    
    return send_file(
        excel_path,
        as_attachment=True,
        download_name='normalized_data.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
