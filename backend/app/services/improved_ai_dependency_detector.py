"""
Improved AI-powered dependency detection with enhanced algorithms
"""
import pandas as pd
import numpy as np
from typing import List, Set, Dict, Tuple
from itertools import combinations
from collections import defaultdict


class ImprovedAIDependencyDetector:
    """Enhanced AI detector for functional and multi-valued dependencies"""
    
    def __init__(self, confidence_threshold: float = 0.90):
        """
        Args:
            confidence_threshold: Minimum confidence (0-1) for accepting dependencies
        """
        self.confidence_threshold = confidence_threshold
        self.min_rows_for_analysis = 3  # Minimum rows needed for meaningful analysis
    
    def detect_all_dependencies(self, table_data: List[Dict], column_names: List[str]) -> Tuple[List[Dict], List[Set[str]]]:
        """
        Detect functional dependencies and candidate keys
        
        Returns:
            Tuple of (functional_dependencies, candidate_keys)
        """
        if not table_data or len(table_data) < self.min_rows_for_analysis:
            return [], []
        
        df = pd.DataFrame(table_data)
        
        # Use actual column names from DataFrame
        actual_columns = list(df.columns)
        
        # Detect functional dependencies
        functional_deps = self._detect_functional_dependencies_improved(df, actual_columns)
        
        # Detect candidate keys
        candidate_keys = self._detect_candidate_keys_improved(df, actual_columns, functional_deps)
        
        return functional_deps, candidate_keys
    
    def _detect_functional_dependencies_improved(self, df: pd.DataFrame, columns: List[str]) -> List[Dict]:
        """Enhanced FD detection with better confidence calculation"""
        fds = []
        n_rows = len(df)
        
        # Test single column dependencies first (most common)
        for det_col in columns:
            # Skip if column has all unique values (it's likely a key, not a determinant)
            if df[det_col].nunique() == n_rows:
                continue
                
            for dep_col in columns:
                if det_col == dep_col:
                    continue
                
                confidence = self._calculate_fd_confidence_improved(df, [det_col], [dep_col])
                
                if confidence >= self.confidence_threshold:
                    fds.append({
                        'determinant': {det_col},
                        'dependent': {dep_col},
                        'confidence': round(confidence, 3)
                    })
        
        # Test composite key dependencies (2 columns) - only if no single column FDs found
        if len(fds) < len(columns) / 2:  # Heuristic: if few FDs found, try composites
            for det_cols in combinations(columns, 2):
                # Skip if combined values are mostly unique
                combined_key = df[list(det_cols)].astype(str).agg('_'.join, axis=1)
                if combined_key.nunique() > n_rows * 0.8:
                    continue
                
                for dep_col in columns:
                    if dep_col in det_cols:
                        continue
                    
                    confidence = self._calculate_fd_confidence_improved(df, list(det_cols), [dep_col])
                    
                    if confidence >= self.confidence_threshold:
                        fds.append({
                            'determinant': set(det_cols),
                            'dependent': {dep_col},
                            'confidence': round(confidence, 3)
                        })
        
        # Remove redundant and trivial FDs
        fds = self._remove_redundant_fds(fds)
        
        return fds
    
    def _calculate_fd_confidence_improved(self, df: pd.DataFrame, determinant: List[str], dependent: List[str]) -> float:
        """
        Improved confidence calculation using multiple metrics
        
        Returns:
            Confidence score from 0 to 1
        """
        try:
            # Handle missing values
            mask = df[determinant + dependent].notna().all(axis=1)
            if mask.sum() == 0:
                return 0.0
            
            df_clean = df[mask]
            
            # Create composite keys
            if len(determinant) == 1:
                det_key = df_clean[determinant[0]].astype(str)
            else:
                det_key = df_clean[determinant].astype(str).agg('_'.join, axis=1)
            
            if len(dependent) == 1:
                dep_key = df_clean[dependent[0]].astype(str)
            else:
                dep_key = df_clean[dependent].astype(str).agg('_'.join, axis=1)
            
            # Method 1: Violation count
            violations = 0
            total_checks = 0
            for det_val in det_key.unique():
                dep_vals = df_clean[det_key == det_val][dependent].drop_duplicates()
                total_checks += 1
                if len(dep_vals) > 1:
                    violations += 1
            
            if total_checks == 0:
                return 0.0
            
            violation_score = 1 - (violations / total_checks)
            
            # Method 2: Determination coefficient
            unique_det = det_key.nunique()
            combined_key = det_key.astype(str) + '_' + dep_key.astype(str)
            unique_combined = combined_key.nunique()
            
            det_coef = unique_det / unique_combined if unique_combined > 0 else 0.0
            
            # Method 3: Consistency ratio
            # For each determinant value, check if dependent values are consistent
            consistency_scores = []
            for det_val in det_key.unique():
                subset = df_clean[det_key == det_val][dependent]
                if len(subset) > 0:
                    # Most common value frequency
                    if len(dependent) == 1:
                        most_common_freq = subset[dependent[0]].value_counts().iloc[0] if len(subset[dependent[0]].value_counts()) > 0 else 0
                        consistency = most_common_freq / len(subset)
                    else:
                        # For composite dependent, check full row duplicates
                        duplicated_rows = subset.duplicated(keep=False).sum()
                        consistency = duplicated_rows / len(subset) if len(subset) > 0 else 0
                    
                    consistency_scores.append(consistency)
            
            avg_consistency = np.mean(consistency_scores) if consistency_scores else 0.0
            
            # Combined confidence (weighted average)
            final_confidence = (
                violation_score * 0.4 +
                det_coef * 0.3 +
                avg_consistency * 0.3
            )
            
            return min(final_confidence, 1.0)
        
        except Exception as e:
            print(f"Error calculating FD confidence: {e}")
            return 0.0
    
    def _detect_candidate_keys_improved(self, df: pd.DataFrame, columns: List[str], fds: List[Dict]) -> List[Set[str]]:
        """Improved candidate key detection"""
        candidate_keys = []
        n_rows = len(df)
        
        # Method 1: Check single columns for uniqueness
        for col in columns:
            # Skip columns with null values for key detection
            if df[col].isnull().any():
                continue
            
            if df[col].nunique() == n_rows:
                # Verify it determines all other columns
                determines_all = True
                for other_col in columns:
                    if other_col == col:
                        continue
                    confidence = self._calculate_fd_confidence_improved(df, [col], [other_col])
                    if confidence < self.confidence_threshold:
                        determines_all = False
                        break
                
                if determines_all:
                    candidate_keys.append({col})
        
        # Method 2: Check composite keys if no single column keys found
        if not candidate_keys:
            for size in range(2, min(len(columns), 5) + 1):  # Check up to 4-column keys
                for col_combo in combinations(columns, size):
                    # Skip if any column has nulls
                    if df[list(col_combo)].isnull().any().any():
                        continue
                    
                    # Check uniqueness
                    composite_key = df[list(col_combo)].astype(str).agg('_'.join, axis=1)
                    if composite_key.nunique() != n_rows:
                        continue
                    
                    # Verify it determines all other columns
                    determines_all = True
                    other_cols = set(columns) - set(col_combo)
                    
                    for other_col in other_cols:
                        confidence = self._calculate_fd_confidence_improved(df, list(col_combo), [other_col])
                        if confidence < self.confidence_threshold:
                            determines_all = False
                            break
                    
                    if determines_all:
                        candidate_keys.append(set(col_combo))
                
                # Stop if we found keys of this size
                if candidate_keys:
                    break
        
        # Method 3: Infer from FDs if still no keys
        if not candidate_keys and fds:
            # Try to find a minimal set of columns that determines everything
            all_cols = set(columns)
            # LIMIT SEARCH DEPTH: for table with many columns, searching all combinations is too slow
            # We limit to searching only for keys up to size 5, which is reasonable for most real DBs
            max_key_size = min(len(columns) + 1, 6)
            
            for size in range(1, max_key_size):
                for col_combo in combinations(columns, size):
                    col_set = set(col_combo)
                    
                    # Check if this set determines all columns via FDs
                    determined = set(col_combo)
                    changed = True
                    max_iterations = 10
                    iteration = 0
                    
                    while changed and iteration < max_iterations:
                        changed = False
                        iteration += 1
                        for fd in fds:
                            if fd['determinant'].issubset(determined) and not fd['dependent'].issubset(determined):
                                determined |= fd['dependent']
                                changed = True
                    
                    if determined == all_cols:
                        # Verify actual uniqueness
                        if len(col_combo) == 1:
                            if df[list(col_combo)[0]].nunique() == n_rows:
                                candidate_keys.append(col_set)
                        else:
                            composite = df[list(col_combo)].astype(str).agg('_'.join, axis=1)
                            if composite.nunique() == n_rows:
                                candidate_keys.append(col_set)
                
                if candidate_keys:
                    break
        
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
    
    def _remove_redundant_fds(self, fds: List[Dict]) -> List[Dict]:
        """Remove redundant functional dependencies"""
        # Remove FDs where dependent is subset of determinant (trivial FDs)
        filtered = [fd for fd in fds if not fd['dependent'].issubset(fd['determinant'])]
        
        # Remove weaker FDs (same determinant and dependent but lower confidence)
        unique_fds = {}
        for fd in filtered:
            key = (frozenset(fd['determinant']), frozenset(fd['dependent']))
            if key not in unique_fds or fd['confidence'] > unique_fds[key]['confidence']:
                unique_fds[key] = fd
        
        # Remove FDs that can be inferred from others (transitive)
        result = list(unique_fds.values())
        
        # Sort by confidence (highest first)
        result.sort(key=lambda x: x['confidence'], reverse=True)
        
        return result
