"""
Shift analyzer module for detecting significant semantic changes.
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class ParadigmShift:
    """Represents a detected paradigm shift."""
    year: int
    term: str
    similarity: float
    context_before: str
    context_after: str
    significance_score: float
    is_significant: bool


class ShiftAnalyzer:
    """
    Analyzes temporal embeddings to detect significant semantic shifts.
    
    Uses statistical methods like permutation tests to determine if
    observed changes in word usage are statistically significant.
    """
    
    def __init__(self, threshold: float = 0.3, significance_level: float = 0.05):
        """
        Initialize the shift analyzer.
        
        Args:
            threshold: Minimum drop in similarity to consider as potential shift
            significance_level: P-value threshold for statistical significance
        """
        self.threshold = threshold
        self.significance_level = significance_level
        
    def compute_similarity_timeline(self, term: str, 
                                     time_slices: List[str],
                                     embedding_model) -> List[Tuple[str, float]]:
        """
        Compute similarity scores for a term across all time slices.
        
        Args:
            term: The term to analyze
            time_slices: List of time slice identifiers
            embedding_model: TemporalEmbedding instance
            
        Returns:
            List of (time_slice, similarity) tuples comparing consecutive periods
        """
        timeline = []
        
        for i in range(len(time_slices) - 1):
            ts1 = time_slices[i]
            ts2 = time_slices[i + 1]
            
            similarity = embedding_model.compute_similarity(term, ts1, ts2)
            timeline.append((ts2, similarity))
            
        return timeline
    
    def detect_drops(self, timeline: List[Tuple[str, float]], 
                     term: str) -> List[ParadigmShift]:
        """
        Detect significant drops in similarity from the timeline.
        
        Args:
            timeline: List of (time_slice, similarity) tuples
            term: The term being analyzed
            
        Returns:
            List of detected paradigm shifts
        """
        shifts = []
        
        for i, (time_slice, similarity) in enumerate(timeline):
            if similarity < self.threshold:
                # Extract year from time slice (e.g., "1990-1995" -> 1995)
                year = int(time_slice.split('-')[-1])
                
                shift = ParadigmShift(
                    year=year,
                    term=term,
                    similarity=similarity,
                    context_before=f"Usage before {year}",
                    context_after=f"Usage after {year}",
                    significance_score=1.0 - similarity,
                    is_significant=True  # Will be refined by permutation test
                )
                shifts.append(shift)
                
        return shifts
    
    def permutation_test(self, term: str, time_slice1: str, 
                         time_slice2: str, embedding_model,
                         n_permutations: int = 1000) -> float:
        """
        Perform permutation test to assess significance of semantic shift.
        
        Args:
            term: The term to test
            time_slice1: First time period
            time_slice2: Second time period
            embedding_model: TemporalEmbedding instance
            n_permutations: Number of permutations for the test
            
        Returns:
            P-value indicating statistical significance
        """
        # Get observed similarity
        observed_similarity = embedding_model.compute_similarity(
            term, time_slice1, time_slice2
        )
        
        # Get all terms for comparison
        vocab = embedding_model.vocabulary
        all_terms = list(vocab.keys())
        
        if len(all_terms) < 10:
            return 1.0  # Not enough data for reliable test
        
        # Count how many random terms show similar or greater change
        count_extreme = 0
        
        for _ in range(n_permutations):
            # Sample random terms
            random_terms = np.random.choice(all_terms, size=min(100, len(all_terms)), 
                                           replace=False)
            
            for random_term in random_terms:
                sim = embedding_model.compute_similarity(random_term, 
                                                        time_slice1, time_slice2)
                if sim <= observed_similarity:
                    count_extreme += 1
        
        # Calculate p-value
        total_comparisons = n_permutations * min(100, len(all_terms))
        p_value = count_extreme / total_comparisons if total_comparisons > 0 else 1.0
        
        return p_value
    
    def analyze_shift(self, term: str, time_slices: List[str], 
                      embedding_model) -> List[ParadigmShift]:
        """
        Complete analysis pipeline for detecting paradigm shifts.
        
        Args:
            term: The term to analyze
            time_slices: List of time slice identifiers
            embedding_model: TemporalEmbedding instance
            
        Returns:
            List of detected paradigm shifts with significance testing
        """
        # Compute similarity timeline
        timeline = self.compute_similarity_timeline(term, time_slices, embedding_model)
        
        # Detect potential shifts
        potential_shifts = self.detect_drops(timeline, term)
        
        # Refine with permutation tests
        validated_shifts = []
        for shift in potential_shifts:
            # Find corresponding time slices
            idx = next(i for i, (ts, _) in enumerate(timeline) 
                      if int(ts.split('-')[-1]) == shift.year)
            ts1 = time_slices[idx]
            ts2 = time_slices[idx + 1]
            
            # Run permutation test
            p_value = self.permutation_test(term, ts1, ts2, embedding_model)
            
            shift.significance_score = 1.0 - p_value
            shift.is_significant = p_value < self.significance_level
            
            if shift.is_significant:
                validated_shifts.append(shift)
        
        return validated_shifts
