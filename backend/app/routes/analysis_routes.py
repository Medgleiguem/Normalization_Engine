"""
Analysis routes - handle normalization analysis (UPDATED)
"""
from flask import Blueprint, request, jsonify, current_app
import os
import uuid
from app.services.excel_parser import ExcelParser
from app.services.normalization_engine import NormalizationEngine
from app.services.improved_report_generator import ImprovedReportGenerator
from app.services.sql_generator import SQLGenerator
from app.services.excel_generator import ExcelGenerator
from app.utils.file_handler import get_output_path

analysis_bp = Blueprint('analysis', __name__)
analysis_cache = {}

@analysis_bp.route('/analyze/<file_id>', methods=['POST'])
def analyze_file(file_id):
    """Perform normalization analysis on uploaded file"""
    try:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        file_path = None
        
        for filename in os.listdir(upload_folder):
            if filename.startswith(file_id):
                file_path = os.path.join(upload_folder, filename)
                break
        
        if not file_path or not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        print(f"Parsing Excel file: {file_path}")
        parser = ExcelParser(file_path)
        tables = parser.parse()
        print(f"Parsed {len(tables)} tables")
        
        if not tables:
            return jsonify({'error': 'No valid tables found in Excel file'}), 400
        
        table = tables[0]
        print(f"Analyzing table: {table.name} with {len(table.columns)} columns")
        
        print("Starting normalization engine...")
        engine = NormalizationEngine(table)
        analysis_result = engine.analyze()
        print(f"Analysis complete. Found {len(analysis_result.normalization_steps)} steps")
        
        analysis_id = str(uuid.uuid4())
        
        report_path = get_output_path(file_id, 'report', 'docx')
        sql_path = get_output_path(file_id, 'schema', 'sql')
        excel_path = get_output_path(file_id, 'normalized', 'xlsx')
        
        # Generate report using improved generator
        print("Generating report with docx-js...")
        result_dict = {
            'analysis_id': analysis_id,
            'original_table': analysis_result.original_table.name,
            'original_nf': analysis_result.current_normal_form.value,
            'final_nf': analysis_result.normalization_steps[-1].to_nf.value if analysis_result.normalization_steps else analysis_result.current_normal_form.value,
            'steps_count': len(analysis_result.normalization_steps),
            'tables_count': len(analysis_result.final_tables),
            'violations_count': len(analysis_result.get_all_violations()),
            'steps': [
                {
                    'from_nf': step.from_nf.value,
                    'to_nf': step.to_nf.value,
                    'violations': len(step.violations_found),
                    'explanation': step.explanation
                }
                for step in analysis_result.normalization_steps
            ]
        }
        report_gen = ImprovedReportGenerator(result_dict)
        report_gen.generate_report(report_path)
        print(f"Report saved to: {report_path}")
        
        # Generate SQL script
        print("Generating SQL script...")
        sql_gen = SQLGenerator(analysis_result)
        sql_script = sql_gen.generate_script()
        with open(sql_path, 'w', encoding='utf-8') as f:
            f.write(sql_script)
        print(f"SQL script saved to: {sql_path}")
        
        print("Generating normalized Excel...")
        excel_gen = ExcelGenerator(analysis_result)
        excel_gen.generate_excel(excel_path)
        print(f"Excel saved to: {excel_path}")
        
        analysis_cache[analysis_id] = {
            'file_id': file_id,
            'result': analysis_result,
            'report_path': report_path,
            'sql_path': sql_path,
            'excel_path': excel_path
        }
        
        response_data = {
            'success': True,
            'analysis_id': analysis_id,
            'original_table': table.name,
            'original_nf': analysis_result.current_normal_form.value,
            'final_nf': analysis_result.normalization_steps[-1].to_nf.value if analysis_result.normalization_steps else analysis_result.current_normal_form.value,
            'steps_count': len(analysis_result.normalization_steps),
            'tables_count': len(analysis_result.final_tables),
            'violations_count': len(analysis_result.get_all_violations()),
            'steps': [
                {
                    'from_nf': step.from_nf.value,
                    'to_nf': step.to_nf.value,
                    'violations': len(step.violations_found),
                    'explanation': step.explanation[:200] + '...' if len(step.explanation) > 200 else step.explanation
                }
                for step in analysis_result.normalization_steps
            ]
        }
        
        return jsonify(response_data), 200
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        current_app.logger.error(f"Analysis error: {str(e)}\n{error_details}")
        print(f"ERROR: {str(e)}")
        print(error_details)
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@analysis_bp.route('/status/<analysis_id>', methods=['GET'])
def get_analysis_status(analysis_id):
    """Get analysis status and results"""
    if analysis_id not in analysis_cache:
        return jsonify({'error': 'Analysis not found'}), 404
    
    cached = analysis_cache[analysis_id]
    result = cached['result']
    
    return jsonify({
        'analysis_id': analysis_id,
        'status': 'completed',
        'original_nf': result.current_normal_form.value,
        'final_nf': result.normalization_steps[-1].to_nf.value if result.normalization_steps else result.current_normal_form.value,
        'tables_count': len(result.final_tables)
    }), 200
