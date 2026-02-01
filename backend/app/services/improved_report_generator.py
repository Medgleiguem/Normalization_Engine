"""
Improved Report Generator - Uses docx-js via Node.js for professional documents
"""
import json
import subprocess
import tempfile
import os
from typing import Dict, Any


class ImprovedReportGenerator:
    """Generate comprehensive normalization analysis reports using docx-js"""
    
    def __init__(self, analysis_result: Dict[str, Any]):
        self.analysis_result = analysis_result
        
        # Convert analysis result to format expected by Node.js script
        self.report_data = self._prepare_report_data()
    
    def _prepare_report_data(self) -> Dict[str, Any]:
        """Prepare data structure for report generation"""
        result = self.analysis_result
        
        return {
            'analysis_id': result.get('analysis_id', 'N/A'),
            'original_table': result.get('original_table', 'Unknown'),
            'original_nf': result.get('original_nf', 'Unnormalized'),
            'final_nf': result.get('final_nf', '1NF'),
            'steps_count': result.get('steps_count', 0),
            'tables_count': result.get('tables_count', 1),
            'violations_count': result.get('violations_count', 0),
            'steps': result.get('steps', [])
        }
    
    def generate_report(self, output_path: str) -> str:
        """Generate report using Node.js docx-js"""
        try:
            # Write analysis data to temp file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                json.dump(self.report_data, temp_file, indent=2)
                temp_path = temp_file.name
            
            # Get the Node.js script path
            script_dir = os.path.dirname(os.path.abspath(__file__))
            node_script = os.path.join(script_dir, 'report_generator.js')
            
            # Check if script exists
            if not os.path.exists(node_script):
                 # Try finding it in the project root as fallback
                project_root = os.path.abspath(os.path.join(script_dir, '..', '..', '..'))
                node_script_fallback = os.path.join(project_root, 'database-normalization-fix', 'report_generator.js')
                if os.path.exists(node_script_fallback):
                     node_script = node_script_fallback
            
            # Run Node.js script
            result = subprocess.run(
                ['node', node_script, temp_path, output_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Clean up temp file
            try:
                os.unlink(temp_path)
            except:
                pass
            
            if result.returncode != 0:
                raise Exception(f"Node.js script failed: {result.stderr}")
            
            # Check if file was created
            if not os.path.exists(output_path):
                raise Exception("Report file was not created")
            
            return output_path
            
        except subprocess.TimeoutExpired:
            raise Exception("Report generation timed out")
        except Exception as e:
            raise Exception(f"Failed to generate report: {str(e)}")
