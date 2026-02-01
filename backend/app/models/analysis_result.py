"""
Data models for normalization analysis results
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
from app.models.table_model import Table

class NormalForm(Enum):
    """Normal form levels"""
    UNNORMALIZED = "Unnormalized"
    FIRST_NF = "1NF"
    SECOND_NF = "2NF"
    THIRD_NF = "3NF"
    BCNF = "BCNF"
    FOURTH_NF = "4NF"
    FIFTH_NF = "5NF"

@dataclass
class Violation:
    """Represents a normalization violation"""
    normal_form: NormalForm
    description: str
    affected_columns: List[str]
    explanation: str
    resolution: str

@dataclass
class NormalizationStep:
    """Represents a single normalization step"""
    from_nf: NormalForm
    to_nf: NormalForm
    violations_found: List[Violation]
    tables_created: List[Table]
    explanation: str
    sql_changes: List[str] = field(default_factory=list)

@dataclass
class AnalysisResult:
    """Complete normalization analysis result"""
    original_table: Table
    current_normal_form: NormalForm
    target_normal_form: NormalForm = NormalForm.FIFTH_NF
    normalization_steps: List[NormalizationStep] = field(default_factory=list)
    final_tables: List[Table] = field(default_factory=list)
    analysis_id: Optional[str] = None
    
    def get_all_violations(self) -> List[Violation]:
        """Get all violations across all steps"""
        violations = []
        for step in self.normalization_steps:
            violations.extend(step.violations_found)
        return violations
    
    def is_fully_normalized(self) -> bool:
        """Check if target normal form was achieved"""
        if not self.normalization_steps:
            return False
        last_step = self.normalization_steps[-1]
        return last_step.to_nf == self.target_normal_form
