"""
Data models for table structure and normalization analysis
"""
from dataclasses import dataclass, field
from typing import List, Set, Dict, Optional, Tuple
from enum import Enum

class DataType(Enum):
    """SQL data types"""
    INTEGER = "INT"
    BIGINT = "BIGINT"
    DECIMAL = "DECIMAL"
    VARCHAR = "VARCHAR"
    TEXT = "TEXT"
    DATE = "DATE"
    DATETIME = "DATETIME"
    BOOLEAN = "BOOLEAN"
    
@dataclass
class Column:
    """Represents a database column"""
    name: str
    data_type: DataType
    max_length: Optional[int] = None
    nullable: bool = True
    unique: bool = False
    sample_values: List = field(default_factory=list)
    
    def to_sql(self) -> str:
        """Generate SQL column definition"""
        sql = f"`{self.name}` {self.data_type.value}"
        if self.max_length and self.data_type == DataType.VARCHAR:
            sql += f"({self.max_length})"
        if not self.nullable:
            sql += " NOT NULL"
        if self.unique:
            sql += " UNIQUE"
        return sql

@dataclass
class FunctionalDependency:
    """Represents a functional dependency X -> Y"""
    determinant: Set[str]  # Left side (X)
    dependent: Set[str]    # Right side (Y)
    confidence: float = 1.0  # Confidence score from AI detection
    
    def __str__(self):
        det = ', '.join(sorted(self.determinant))
        dep = ', '.join(sorted(self.dependent))
        return f"{{{det}}} -> {{{dep}}} (confidence: {self.confidence:.2f})"

@dataclass
class MultiValuedDependency:
    """Represents a multi-valued dependency X ->-> Y"""
    determinant: Set[str]
    dependent: Set[str]
    confidence: float = 1.0
    
    def __str__(self):
        det = ', '.join(sorted(self.determinant))
        dep = ', '.join(sorted(self.dependent))
        return f"{{{det}}} ->> {{{dep}}} (confidence: {self.confidence:.2f})"

@dataclass
class Table:
    """Represents a database table"""
    name: str
    columns: List[Column]
    primary_key: Set[str] = field(default_factory=set)
    candidate_keys: List[Set[str]] = field(default_factory=list)
    foreign_keys: Dict[str, Tuple[str, str]] = field(default_factory=dict)  # column -> (ref_table, ref_column)
    functional_dependencies: List[FunctionalDependency] = field(default_factory=list)
    multi_valued_dependencies: List[MultiValuedDependency] = field(default_factory=list)
    data: List[Dict] = field(default_factory=list)  # Sample data rows
    
    def get_column(self, name: str) -> Optional[Column]:
        """Get column by name"""
        for col in self.columns:
            if col.name == name:
                return col
        return None
    
    def get_column_names(self) -> List[str]:
        """Get all column names"""
        return [col.name for col in self.columns]
