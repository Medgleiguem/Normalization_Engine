"""
Excel file parser - extracts table structure and data from Excel files
"""
import pandas as pd
import openpyxl
from typing import List, Dict, Any, Optional
from app.models.table_model import Table, Column, DataType
import re

class ExcelParser:
    """Parse Excel files and extract table structures"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.workbook = None
        
    def parse(self) -> List[Table]:
        """Parse Excel file and return list of tables (one per sheet)"""
        tables = []
        
        # Read Excel file
        excel_file = pd.ExcelFile(self.file_path)
        
        for sheet_name in excel_file.sheet_names:
            # Skip metadata sheets
            if sheet_name.lower() in ['metadata', 'dependencies', 'info']:
                continue
                
            df = pd.read_excel(self.file_path, sheet_name=sheet_name)
            
            # Skip empty sheets
            if df.empty:
                continue
            
            table = self._dataframe_to_table(df, sheet_name)
            tables.append(table)
        
        return tables
    
    def _dataframe_to_table(self, df: pd.DataFrame, table_name: str) -> Table:
        """Convert pandas DataFrame to Table model"""
        # Clean table name
        clean_name = self._clean_name(table_name)
        
        # Extract columns
        columns = []
        data_rows = []
        
        for col_name in df.columns:
            column = self._analyze_column(df, col_name)
            columns.append(column)
        
        # Convert data to list of dictionaries
        data_rows = df.head(100).to_dict('records')  # Keep first 100 rows for analysis
        
        table = Table(
            name=clean_name,
            columns=columns,
            data=data_rows
        )
        
        return table
    
    def _analyze_column(self, df: pd.DataFrame, col_name: str) -> Column:
        """Analyze a column and determine its properties"""
        clean_name = self._clean_name(col_name)
        series = df[col_name]
        
        # Determine data type
        data_type = self._infer_data_type(series)
        
        # Calculate max length for VARCHAR
        max_length = None
        if data_type == DataType.VARCHAR:
            max_length = int(series.astype(str).str.len().max())
            max_length = max(max_length, 50)  # Minimum 50
            max_length = min(max_length, 255)  # Maximum 255
        
        # Check if nullable
        nullable = series.isnull().any()
        
        # Check if unique
        unique = len(series.unique()) == len(series.dropna())
        
        # Get sample values
        sample_values = series.dropna().head(5).tolist()
        
        return Column(
            name=clean_name,
            data_type=data_type,
            max_length=max_length,
            nullable=nullable,
            unique=unique,
            sample_values=sample_values
        )
    
    def _infer_data_type(self, series: pd.Series) -> DataType:
        """Infer SQL data type from pandas series"""
        # Drop null values for type inference
        series_clean = series.dropna()
        
        if len(series_clean) == 0:
            return DataType.VARCHAR
        
        # Check for boolean
        if series_clean.dtype == bool or set(series_clean.unique()).issubset({0, 1, True, False}):
            return DataType.BOOLEAN
        
        # Check for integer
        if pd.api.types.is_integer_dtype(series_clean):
            max_val = series_clean.max()
            if max_val > 2147483647:  # Max INT value
                return DataType.BIGINT
            return DataType.INTEGER
        
        # Check for float/decimal
        if pd.api.types.is_float_dtype(series_clean):
            return DataType.DECIMAL
        
        # Check for datetime
        if pd.api.types.is_datetime64_any_dtype(series_clean):
            return DataType.DATETIME
        
        # Try to parse as date
        try:
            pd.to_datetime(series_clean, errors='raise')
            return DataType.DATE
        except:
            pass
        
        # Check string length for TEXT vs VARCHAR
        if pd.api.types.is_string_dtype(series_clean) or pd.api.types.is_object_dtype(series_clean):
            max_len = series_clean.astype(str).str.len().max()
            if max_len > 500:
                return DataType.TEXT
            return DataType.VARCHAR
        
        # Default to VARCHAR
        return DataType.VARCHAR
    
    def _clean_name(self, name: str) -> str:
        """Clean column/table names for SQL compatibility"""
        # Remove special characters, replace spaces with underscores
        clean = re.sub(r'[^\w\s]', '', str(name))
        clean = re.sub(r'\s+', '_', clean)
        clean = clean.lower().strip('_')
        
        # Ensure it doesn't start with a number
        if clean and clean[0].isdigit():
            clean = 'col_' + clean
        
        return clean or 'unnamed'
