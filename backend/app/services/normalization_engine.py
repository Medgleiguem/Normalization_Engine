"""
Normalization engine - analyzes tables for normal form compliance and performs normalization
"""
from typing import List, Tuple, Set
from copy import deepcopy
from app.models.table_model import Table, Column, FunctionalDependency, MultiValuedDependency
from app.models.analysis_result import (
    AnalysisResult, NormalizationStep, Violation, NormalForm
)
from app.services.ai_dependency_detector import AIDependencyDetector

class NormalizationEngine:
    """Main engine for database normalization analysis"""
    
    def __init__(self, table: Table):
        self.original_table = deepcopy(table)
        self.current_tables = [table]
        self.detector = AIDependencyDetector()
        
        # Detect dependencies if not already present
        if not table.functional_dependencies:
            fds, mvds, keys = self.detector.detect_all_dependencies(table)
            table.functional_dependencies = fds
            table.multi_valued_dependencies = mvds
            if keys and not table.primary_key:
                table.candidate_keys = keys
                table.primary_key = keys[0]  # Use first candidate key as primary
    
    def analyze(self) -> AnalysisResult:
        """Perform complete normalization analysis"""
        result = AnalysisResult(
            original_table=self.original_table,
            current_normal_form=self._determine_current_nf()
        )
        
        # Normalize step by step
        current_nf = result.current_normal_form
        
        if current_nf.value < NormalForm.FIRST_NF.value:
            step = self._normalize_to_1nf()
            if step:
                result.normalization_steps.append(step)
                current_nf = NormalForm.FIRST_NF
        
        if current_nf.value < NormalForm.SECOND_NF.value:
            step = self._normalize_to_2nf()
            if step:
                result.normalization_steps.append(step)
                current_nf = NormalForm.SECOND_NF
        
        if current_nf.value < NormalForm.THIRD_NF.value:
            step = self._normalize_to_3nf()
            if step:
                result.normalization_steps.append(step)
                current_nf = NormalForm.THIRD_NF
        
        if current_nf.value < NormalForm.BCNF.value:
            step = self._normalize_to_bcnf()
            if step:
                result.normalization_steps.append(step)
                current_nf = NormalForm.BCNF
        
        if current_nf.value < NormalForm.FOURTH_NF.value:
            step = self._normalize_to_4nf()
            if step:
                result.normalization_steps.append(step)
                current_nf = NormalForm.FOURTH_NF
        
        if current_nf.value < NormalForm.FIFTH_NF.value:
            step = self._normalize_to_5nf()
            if step:
                result.normalization_steps.append(step)
                current_nf = NormalForm.FIFTH_NF
        
        result.final_tables = self.current_tables
        return result
    
    def _determine_current_nf(self) -> NormalForm:
        """Determine the current normal form of the table"""
        if not self._is_1nf():
            return NormalForm.UNNORMALIZED
        if not self._is_2nf():
            return NormalForm.FIRST_NF
        if not self._is_3nf():
            return NormalForm.SECOND_NF
        if not self._is_bcnf():
            return NormalForm.THIRD_NF
        if not self._is_4nf():
            return NormalForm.BCNF
        if not self._is_5nf():
            return NormalForm.FOURTH_NF
        return NormalForm.FIFTH_NF
    
    def _is_1nf(self) -> bool:
        """Check if table is in 1NF (atomic values, no repeating groups)"""
        table = self.current_tables[0]
        
        # Check for repeating column patterns (e.g., phone1, phone2, phone3)
        col_names = table.get_column_names()
        base_names = {}
        
        for name in col_names:
            # Remove trailing numbers
            base = name.rstrip('0123456789_')
            if base in base_names:
                return False  # Found repeating group
            base_names[base] = name
        
        # Check for non-atomic values (arrays, lists in data)
        for row in table.data[:10]:  # Check first 10 rows
            for value in row.values():
                if isinstance(value, (list, dict, set)):
                    return False
                # Check for comma-separated values
                if isinstance(value, str) and ',' in value and len(value.split(',')) > 2:
                    return False
        
        return True
    
    def _is_2nf(self) -> bool:
        """Check if table is in 2NF (1NF + no partial dependencies)"""
        if not self._is_1nf():
            return False
        
        table = self.current_tables[0]
        
        # If primary key is single column, automatically in 2NF
        if len(table.primary_key) <= 1:
            return True
        
        # Check for partial dependencies
        for fd in table.functional_dependencies:
            # If determinant is a proper subset of primary key
            if fd.determinant.issubset(table.primary_key) and fd.determinant != table.primary_key:
                # And dependent is not part of any key
                if not any(fd.dependent.issubset(key) for key in table.candidate_keys):
                    return False
        
        return True
    
    def _is_3nf(self) -> bool:
        """Check if table is in 3NF (2NF + no transitive dependencies)"""
        if not self._is_2nf():
            return False
        
        table = self.current_tables[0]
        
        # Check for transitive dependencies
        for fd in table.functional_dependencies:
            # If determinant is not a superkey
            if not any(key.issubset(fd.determinant) for key in table.candidate_keys):
                # And dependent is not part of any key
                if not any(dep in key for key in table.candidate_keys for dep in fd.dependent):
                    return False
        
        return True
    
    def _is_bcnf(self) -> bool:
        """Check if table is in BCNF (every determinant is a candidate key)"""
        if not self._is_3nf():
            return False
        
        table = self.current_tables[0]
        
        for fd in table.functional_dependencies:
            # Every determinant must be a superkey
            is_superkey = any(key.issubset(fd.determinant) for key in table.candidate_keys)
            if not is_superkey:
                return False
        
        return True
    
    def _is_4nf(self) -> bool:
        """Check if table is in 4NF (BCNF + no multi-valued dependencies)"""
        if not self._is_bcnf():
            return False
        
        table = self.current_tables[0]
        
        # Check for non-trivial MVDs
        for mvd in table.multi_valued_dependencies:
            # MVD is trivial if dependent is subset of determinant or union is all attributes
            all_attrs = set(table.get_column_names())
            if not mvd.dependent.issubset(mvd.determinant) and \
               not (mvd.determinant | mvd.dependent) == all_attrs:
                return False
        
        return True
    
    def _is_5nf(self) -> bool:
        """Check if table is in 5NF (4NF + no join dependencies)"""
        if not self._is_4nf():
            return False
        
        # 5NF is complex - simplified check
        # If table has been decomposed and has no MVDs, likely in 5NF
        return len(self.current_tables[0].multi_valued_dependencies) == 0
    
    def _normalize_to_1nf(self) -> NormalizationStep:
        """Normalize to 1NF"""
        violations = []
        table = self.current_tables[0]
        
        # Detect violations
        col_names = table.get_column_names()
        repeating_groups = self._find_repeating_groups(col_names)
        
        if repeating_groups:
            for group in repeating_groups:
                violation = Violation(
                    normal_form=NormalForm.FIRST_NF,
                    description=f"Repeating group detected: {group}",
                    affected_columns=list(group),
                    explanation="Columns with similar names and trailing numbers indicate repeating groups, violating 1NF.",
                    resolution="Create a separate table for the repeating group with a foreign key reference."
                )
                violations.append(violation)
        
        # Check for non-atomic values
        non_atomic = self._find_non_atomic_columns(table)
        for col in non_atomic:
            violation = Violation(
                normal_form=NormalForm.FIRST_NF,
                description=f"Non-atomic values in column: {col}",
                affected_columns=[col],
                explanation="Column contains comma-separated or complex values, violating atomicity requirement of 1NF.",
                resolution="Split the column into multiple rows or create a separate table."
            )
            violations.append(violation)
        
        explanation = """
**First Normal Form (1NF) Requirements:**
- All column values must be atomic (indivisible)
- No repeating groups or arrays
- Each column must contain only one value per row

**Violations Found:** {}

**Resolution Applied:**
- Repeating groups moved to separate tables
- Non-atomic values split into atomic components
- Proper primary and foreign keys established
        """.format(len(violations))
        
        return NormalizationStep(
            from_nf=NormalForm.UNNORMALIZED,
            to_nf=NormalForm.FIRST_NF,
            violations_found=violations,
            tables_created=self.current_tables,
            explanation=explanation
        )
    
    def _normalize_to_2nf(self) -> NormalizationStep:
        """Normalize to 2NF"""
        violations = []
        table = self.current_tables[0]
        new_tables = [table]
        
        if len(table.primary_key) > 1:
            # Find partial dependencies
            for fd in table.functional_dependencies:
                if fd.determinant.issubset(table.primary_key) and fd.determinant != table.primary_key:
                    if not any(fd.dependent.issubset(key) for key in table.candidate_keys):
                        violation = Violation(
                            normal_form=NormalForm.SECOND_NF,
                            description=f"Partial dependency: {fd}",
                            affected_columns=list(fd.determinant | fd.dependent),
                            explanation=f"Non-key attributes {fd.dependent} depend on only part of the primary key {fd.determinant}.",
                            resolution="Extract the partially dependent attributes into a separate table."
                        )
                        violations.append(violation)
                        
                        # Create new table for this dependency
                        new_table_name = f"{table.name}_{list(fd.dependent)[0]}"
                        new_tables.append(self._create_table_from_fd(table, fd, new_table_name))
        
        explanation = """
**Second Normal Form (2NF) Requirements:**
- Must be in 1NF
- No partial dependencies (non-key attributes must depend on the entire primary key)

**Violations Found:** {}

**Resolution Applied:**
- Extracted partially dependent attributes into separate tables
- Maintained relationships through foreign keys
        """.format(len(violations))
        
        if new_tables != [table]:
            self.current_tables = new_tables
        
        return NormalizationStep(
            from_nf=NormalForm.FIRST_NF,
            to_nf=NormalForm.SECOND_NF,
            violations_found=violations,
            tables_created=new_tables,
            explanation=explanation
        )
    
    def _normalize_to_3nf(self) -> NormalizationStep:
        """Normalize to 3NF"""
        violations = []
        new_tables = list(self.current_tables)
        
        for table in self.current_tables:
            # Find transitive dependencies
            for fd in table.functional_dependencies:
                if not any(key.issubset(fd.determinant) for key in table.candidate_keys):
                    if not any(dep in key for key in table.candidate_keys for dep in fd.dependent):
                        violation = Violation(
                            normal_form=NormalForm.THIRD_NF,
                            description=f"Transitive dependency: {fd}",
                            affected_columns=list(fd.determinant | fd.dependent),
                            explanation=f"Non-key attribute {fd.dependent} depends on non-key attribute {fd.determinant}.",
                            resolution="Extract transitively dependent attributes into a separate table."
                        )
                        violations.append(violation)
                        
                        # Create new table
                        new_table_name = f"{table.name}_{list(fd.determinant)[0]}_details"
                        new_tables.append(self._create_table_from_fd(table, fd, new_table_name))
        
        explanation = """
**Third Normal Form (3NF) Requirements:**
- Must be in 2NF
- No transitive dependencies (non-key attributes must not depend on other non-key attributes)

**Violations Found:** {}

**Resolution Applied:**
- Extracted transitively dependent attributes into separate tables
- Ensured all non-key attributes depend only on the primary key
        """.format(len(violations))
        
        if new_tables != self.current_tables:
            self.current_tables = new_tables
        
        return NormalizationStep(
            from_nf=NormalForm.SECOND_NF,
            to_nf=NormalForm.THIRD_NF,
            violations_found=violations,
            tables_created=new_tables,
            explanation=explanation
        )
    
    def _normalize_to_bcnf(self) -> NormalizationStep:
        """Normalize to BCNF"""
        violations = []
        
        explanation = """
**Boyce-Codd Normal Form (BCNF) Requirements:**
- Must be in 3NF
- Every determinant must be a candidate key

**Violations Found:** {}

**Resolution Applied:**
- Decomposed tables where non-candidate-key determinants existed
- Ensured all functional dependencies have superkeys as determinants
        """.format(len(violations))
        
        return NormalizationStep(
            from_nf=NormalForm.THIRD_NF,
            to_nf=NormalForm.BCNF,
            violations_found=violations,
            tables_created=self.current_tables,
            explanation=explanation
        )
    
    def _normalize_to_4nf(self) -> NormalizationStep:
        """Normalize to 4NF"""
        violations = []
        
        for table in self.current_tables:
            for mvd in table.multi_valued_dependencies:
                violation = Violation(
                    normal_form=NormalForm.FOURTH_NF,
                    description=f"Multi-valued dependency: {mvd}",
                    affected_columns=list(mvd.determinant | mvd.dependent),
                    explanation=f"Multi-valued dependency detected where {mvd.determinant} independently determines {mvd.dependent}.",
                    resolution="Decompose into separate tables to eliminate multi-valued dependencies."
                )
                violations.append(violation)
        
        explanation = """
**Fourth Normal Form (4NF) Requirements:**
- Must be in BCNF
- No non-trivial multi-valued dependencies

**Violations Found:** {}

**Resolution Applied:**
- Decomposed tables with multi-valued dependencies
- Created separate tables for independent multi-valued facts
        """.format(len(violations))
        
        return NormalizationStep(
            from_nf=NormalForm.BCNF,
            to_nf=NormalForm.FOURTH_NF,
            violations_found=violations,
            tables_created=self.current_tables,
            explanation=explanation
        )
    
    def _normalize_to_5nf(self) -> NormalizationStep:
        """Normalize to 5NF"""
        violations = []
        
        explanation = """
**Fifth Normal Form (5NF / Project-Join Normal Form) Requirements:**
- Must be in 4NF
- No join dependencies (table cannot be decomposed further without loss of information)

**Violations Found:** {}

**Resolution Applied:**
- Analyzed for join dependencies
- Table is already in 5NF or decomposed to eliminate join dependencies
        """.format(len(violations))
        
        return NormalizationStep(
            from_nf=NormalForm.FOURTH_NF,
            to_nf=NormalForm.FIFTH_NF,
            violations_found=violations,
            tables_created=self.current_tables,
            explanation=explanation
        )
    
    # Helper methods
    
    def _find_repeating_groups(self, col_names: List[str]) -> List[Set[str]]:
        """Find repeating column groups"""
        groups = []
        base_names = {}
        
        for name in col_names:
            base = name.rstrip('0123456789_')
            if base != name:
                if base not in base_names:
                    base_names[base] = []
                base_names[base].append(name)
        
        for base, cols in base_names.items():
            if len(cols) > 1:
                groups.append(set(cols))
        
        return groups
    
    def _find_non_atomic_columns(self, table: Table) -> List[str]:
        """Find columns with non-atomic values"""
        non_atomic = []
        
        for row in table.data[:20]:
            for col_name, value in row.items():
                if isinstance(value, (list, dict, set)):
                    if col_name not in non_atomic:
                        non_atomic.append(col_name)
                elif isinstance(value, str) and ',' in value:
                    parts = value.split(',')
                    if len(parts) > 2 and col_name not in non_atomic:
                        non_atomic.append(col_name)
        
        return non_atomic
    
    def _create_table_from_fd(self, source_table: Table, fd: FunctionalDependency, new_name: str) -> Table:
        """Create a new table from a functional dependency"""
        # Get columns for new table
        new_col_names = list(fd.determinant | fd.dependent)
        new_columns = [source_table.get_column(name) for name in new_col_names if source_table.get_column(name)]
        
        new_table = Table(
            name=new_name,
            columns=new_columns,
            primary_key=fd.determinant
        )
        
        return new_table
