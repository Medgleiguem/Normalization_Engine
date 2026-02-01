"""
AI-powered dependency detection using statistical analysis and pattern recognition
"""
import pandas as pd
import numpy as np
from typing import List, Set, Dict, Tuple
from itertools import combinations
from sklearn.metrics import mutual_info_score
from app.models.table_model import Table, FunctionalDependency, MultiValuedDependency

class AIDependencyDetector:
    """Detect functional and multi-valued dependencies using AI/ML techniques"""
    
    def __init__(self, confidence_threshold: float = 0.85):
        self.confidence_threshold = confidence_threshold
    
    def detect_all_dependencies(self, table: Table) -> Tuple[List[FunctionalDependency], List[MultiValuedDependency], List[Set[str]]]:
        """
        Detect all dependencies in a table
        Returns: (functional_dependencies, multi_valued_dependencies, candidate_keys)
        """
        if not table.data or len(table.data) < 2:
            return [], [], []
        
        df = pd.DataFrame(table.data)
        
        # IMPORTANT: Use the actual DataFrame column names, not the cleaned Table column names
        # The DataFrame has the original Excel column names
        column_names = list(df.columns)
        
        # Detect functional dependencies
        functional_deps = self._detect_functional_dependencies(df, column_names)
        
        # Detect candidate keys
        candidate_keys = self._detect_candidate_keys(df, column_names, functional_deps)
        
        # Detect multi-valued dependencies
        mvds = self._detect_multi_valued_dependencies(df, column_names, candidate_keys)
        
        # Convert column names back to cleaned names for the Table model
        # Create a mapping from original to cleaned names
        original_to_cleaned = {col.name: table.get_column_names()[i] 
                               for i, col in enumerate(table.columns)}
        
        # Update functional dependencies with cleaned names
        cleaned_fds = []
        for fd in functional_deps:
            cleaned_fd = FunctionalDependency(
                determinant={original_to_cleaned.get(col, col) for col in fd.determinant},
                dependent={original_to_cleaned.get(col, col) for col in fd.dependent},
                confidence=fd.confidence
            )
            cleaned_fds.append(cleaned_fd)
        
        # Update candidate keys with cleaned names
        cleaned_keys = []
        for key in candidate_keys:
            cleaned_key = {original_to_cleaned.get(col, col) for col in key}
            cleaned_keys.append(cleaned_key)
        
        # Update MVDs with cleaned names
        cleaned_mvds = []
        for mvd in mvds:
            cleaned_mvd = MultiValuedDependency(
                determinant={original_to_cleaned.get(col, col) for col in mvd.determinant},
                dependent={original_to_cleaned.get(col, col) for col in mvd.dependent},
                confidence=mvd.confidence
            )
            cleaned_mvds.append(cleaned_mvd)
        
        return cleaned_fds, cleaned_mvds, cleaned_keys
    
    def _detect_functional_dependencies(self, df: pd.DataFrame, columns: List[str]) -> List[FunctionalDependency]:
        """Detect functional dependencies using determination coefficient"""
        fds = []
        
        # Test single column dependencies first
        for det_col in columns:
            for dep_col in columns:
                if det_col == dep_col:
                    continue
                
                confidence = self._calculate_fd_confidence(df, [det_col], [dep_col])
                
                if confidence >= self.confidence_threshold:
                    fd = FunctionalDependency(
                        determinant={det_col},
                        dependent={dep_col},
                        confidence=confidence
                    )
                    fds.append(fd)
        
        # Test composite key dependencies (2 columns)
        for det_cols in combinations(columns, 2):
            for dep_col in columns:
                if dep_col in det_cols:
                    continue
                
                confidence = self._calculate_fd_confidence(df, list(det_cols), [dep_col])
                
                if confidence >= self.confidence_threshold:
                    fd = FunctionalDependency(
                        determinant=set(det_cols),
                        dependent={dep_col},
                        confidence=confidence
                    )
                    fds.append(fd)
        
        # Remove redundant dependencies
        fds = self._remove_redundant_fds(fds)
        
        return fds
    
    def _calculate_fd_confidence(self, df: pd.DataFrame, determinant: List[str], dependent: List[str]) -> float:
        """
        Calculate confidence that determinant -> dependent holds
        Uses determination coefficient: ratio of unique determinant values to unique (determinant, dependent) pairs
        """
        try:
            # Create composite keys
            det_key = df[determinant].astype(str).agg('_'.join, axis=1)
            dep_key = df[dependent].astype(str).agg('_'.join, axis=1)
            combined_key = det_key + '_' + dep_key
            
            # Count unique values
            unique_det = det_key.nunique()
            unique_combined = combined_key.nunique()
            
            if unique_det == 0:
                return 0.0
            
            # Perfect FD: unique_det == unique_combined
            confidence = unique_det / unique_combined if unique_combined > 0 else 0.0
            
            # Also check for violations
            violations = 0
            for det_val in det_key.unique():
                dep_vals = df[det_key == det_val][dependent].drop_duplicates()
                if len(dep_vals) > 1:
                    violations += 1
            
            violation_penalty = violations / unique_det if unique_det > 0 else 0
            confidence = confidence * (1 - violation_penalty)
            
            return min(confidence, 1.0)
        
        except Exception:
            return 0.0
    
    def _detect_candidate_keys(self, df: pd.DataFrame, columns: List[str], fds: List[FunctionalDependency]) -> List[Set[str]]:
        """Detect candidate keys using uniqueness analysis"""
        candidate_keys = []
        
        # Check single column keys
        for col in columns:
            if df[col].nunique() == len(df) and not df[col].isnull().any():
                candidate_keys.append({col})
        
        # If no single column keys, check composite keys
        if not candidate_keys:
            for size in range(2, min(len(columns), 4) + 1):  # Check up to 4 columns
                for col_combo in combinations(columns, size):
                    composite_key = df[list(col_combo)].astype(str).agg('_'.join, axis=1)
                    if composite_key.nunique() == len(df):
                        # Check if this determines all other columns
                        determines_all = True
                        other_cols = set(columns) - set(col_combo)
                        
                        for other_col in other_cols:
                            confidence = self._calculate_fd_confidence(df, list(col_combo), [other_col])
                            if confidence < self.confidence_threshold:
                                determines_all = False
                                break
                        
                        if determines_all:
                            candidate_keys.append(set(col_combo))
                
                if candidate_keys:
                    break  # Found keys of this size, don't check larger
        
        # Remove superkeys (keys that contain other keys)
        minimal_keys = []
        for key in candidate_keys:
            is_minimal = True
            for other_key in candidate_keys:
                if other_key != key and other_key.issubset(key):
                    is_minimal = False
                    break
            if is_minimal:
                minimal_keys.append(key)
        
        return minimal_keys if minimal_keys else candidate_keys
    
    def _detect_multi_valued_dependencies(self, df: pd.DataFrame, columns: List[str], candidate_keys: List[Set[str]]) -> List[MultiValuedDependency]:
        """Detect multi-valued dependencies"""
        mvds = []
        
        if not candidate_keys:
            return mvds
        
        # For each candidate key, check for MVDs
        for key in candidate_keys:
            key_list = list(key)
            other_cols = [col for col in columns if col not in key]
            
            # Check pairs of non-key columns for independence
            for col_a, col_b in combinations(other_cols, 2):
                # Check if col_a and col_b are independent given the key
                confidence = self._calculate_mvd_confidence(df, key_list, col_a, col_b)
                
                if confidence >= self.confidence_threshold:
                    mvd = MultiValuedDependency(
                        determinant=key,
                        dependent={col_a},
                        confidence=confidence
                    )
                    mvds.append(mvd)
        
        return mvds
    
    def _calculate_mvd_confidence(self, df: pd.DataFrame, determinant: List[str], col_a: str, col_b: str) -> float:
        """
        Calculate confidence for MVD: determinant ->> col_a
        MVD exists if col_a values are independent of col_b values for each determinant value
        """
        try:
            det_key = df[determinant].astype(str).agg('_'.join, axis=1)
            
            independence_score = 0
            count = 0
            
            for det_val in det_key.unique():
                subset = df[det_key == det_val]
                
                if len(subset) < 2:
                    continue
                
                # Check if col_a values repeat with different col_b values
                a_values = subset[col_a].unique()
                b_values = subset[col_b].unique()
                
                if len(a_values) > 1 and len(b_values) > 1:
                    # Calculate mutual information (lower = more independent)
                    mi = mutual_info_score(subset[col_a].astype(str), subset[col_b].astype(str))
                    
                    # Normalize by entropy
                    max_mi = min(
                        -np.sum(subset[col_a].value_counts(normalize=True) * np.log2(subset[col_a].value_counts(normalize=True) + 1e-10)),
                        -np.sum(subset[col_b].value_counts(normalize=True) * np.log2(subset[col_b].value_counts(normalize=True) + 1e-10))
                    )
                    
                    if max_mi > 0:
                        independence_score += 1 - (mi / max_mi)
                        count += 1
            
            return independence_score / count if count > 0 else 0.0
        
        except Exception:
            return 0.0
    
    def _remove_redundant_fds(self, fds: List[FunctionalDependency]) -> List[FunctionalDependency]:
        """Remove redundant functional dependencies"""
        # Remove FDs where dependent is subset of determinant
        filtered = [fd for fd in fds if not fd.dependent.issubset(fd.determinant)]
        
        # Remove weaker FDs (same determinant and dependent but lower confidence)
        unique_fds = {}
        for fd in filtered:
            key = (frozenset(fd.determinant), frozenset(fd.dependent))
            if key not in unique_fds or fd.confidence > unique_fds[key].confidence:
                unique_fds[key] = fd
        
        return list(unique_fds.values())
