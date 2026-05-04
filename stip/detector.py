"""
Main detector module for paradigm shift detection.
"""

import json
import os
from typing import List, Dict, Optional, Union
from pathlib import Path
from collections import defaultdict

from .embedding import TemporalEmbedding
from .shift_analyzer import ShiftAnalyzer, ParadigmShift


class ParadigmShiftDetector:
    """
    Main class for detecting semantic paradigm shifts in research literature.
    
    This class orchestrates the entire pipeline from data loading to shift detection,
    enabling users to identify when the meaning of scientific terms changes over time.
    
    Example:
        >>> detector = ParadigmShiftDetector(
        ...     corpus_path="./data/arxiv_abstracts.jsonl",
        ...     term="attention"
        ... )
        >>> shifts = detector.detect_shifts()
        >>> for shift in shifts:
        ...     print(f"Shift detected in {shift.year}")
    """
    
    def __init__(self, 
                 corpus_path: str,
                 term: str,
                 time_slice_years: int = 5,
                 embedding_dim: int = 300,
                 threshold: float = 0.3):
        """
        Initialize the paradigm shift detector.
        
        Args:
            corpus_path: Path to JSONL file with abstracts (format: {"year": ..., "text": ...})
            term: The term to analyze for semantic shifts
            time_slice_years: Number of years per time slice (default: 5)
            embedding_dim: Dimension of embedding vectors
            threshold: Similarity threshold for detecting shifts
        """
        self.corpus_path = corpus_path
        self.term = term.lower()
        self.time_slice_years = time_slice_years
        self.embedding_dim = embedding_dim
        
        # Initialize components
        self.embedding_model = TemporalEmbedding(embedding_dim=embedding_dim)
        self.analyzer = ShiftAnalyzer(threshold=threshold)
        
        # Data storage
        self.documents_by_slice: Dict[str, List[str]] = defaultdict(list)
        self.time_slices: List[str] = []
        
    def load_corpus(self) -> None:
        """
        Load and preprocess the corpus from JSONL file.
        
        Expected JSONL format:
            {"year": 1995, "title": "...", "abstract": "..."}
            {"year": 1996, "title": "...", "abstract": "..."}
        """
        if not os.path.exists(self.corpus_path):
            raise FileNotFoundError(f"Corpus file not found: {self.corpus_path}")
        
        print(f"Loading corpus from {self.corpus_path}...")
        
        with open(self.corpus_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    doc = json.loads(line.strip())
                    year = doc.get('year')
                    text = doc.get('abstract', '') + ' ' + doc.get('title', '')
                    
                    if year and text.strip():
                        # Assign to time slice
                        slice_start = (year // self.time_slice_years) * self.time_slice_years
                        slice_end = slice_start + self.time_slice_years - 1
                        time_slice = f"{slice_start}-{slice_end}"
                        
                        self.documents_by_slice[time_slice].append(text)
                        
                except json.JSONDecodeError as e:
                    print(f"Warning: Skipping invalid JSON at line {line_num}: {e}")
                    continue
        
        # Sort time slices chronologically
        self.time_slices = sorted(self.documents_by_slice.keys(), 
                                  key=lambda x: int(x.split('-')[0]))
        
        print(f"Loaded documents into {len(self.time_slices)} time slices:")
        for ts in self.time_slices:
            print(f"  {ts}: {len(self.documents_by_slice[ts])} documents")
    
    def build_embeddings(self) -> None:
        """
        Build temporal embeddings for all time slices.
        """
        if not self.time_slices:
            raise ValueError("No time slices loaded. Call load_corpus() first.")
        
        print("\nBuilding temporal embeddings...")
        
        for time_slice in self.time_slices:
            docs = self.documents_by_slice[time_slice]
            if len(docs) < 10:
                print(f"  Skipping {time_slice}: insufficient documents ({len(docs)})")
                continue
                
            print(f"  Processing {time_slice} ({len(docs)} documents)...")
            self.embedding_model.fit_time_slice(docs, time_slice)
        
        print("Embedding construction complete.")
    
    def detect_shifts(self) -> List[ParadigmShift]:
        """
        Detect paradigm shifts for the target term.
        
        Returns:
            List of detected ParadigmShift objects
        """
        if not self.time_slices:
            self.load_corpus()
        
        if not self.embedding_model.vocabulary:
            self.build_embeddings()
        
        print(f"\nAnalyzing semantic shifts for term: '{self.term}'")
        
        # Check if term exists in vocabulary
        if self.term not in self.embedding_model.vocabulary:
            print(f"Warning: Term '{self.term}' not found in vocabulary.")
            print("Available terms (sample):", 
                  list(self.embedding_model.vocabulary.keys())[:20])
            return []
        
        # Run shift analysis
        shifts = self.analyzer.analyze_shift(
            self.term, 
            self.time_slices, 
            self.embedding_model
        )
        
        print(f"\nDetected {len(shifts)} significant paradigm shift(s):")
        for shift in shifts:
            print(f"  Year {shift.year}: similarity={shift.similarity:.3f}, "
                  f"significance={shift.significance_score:.3f}")
        
        return shifts
    
    def get_similarity_timeline(self) -> List[Dict]:
        """
        Get the full similarity timeline for visualization.
        
        Returns:
            List of dictionaries with time_slice and similarity score
        """
        if not self.time_slices:
            self.load_corpus()
        
        if not self.embedding_model.vocabulary:
            self.build_embeddings()
        
        timeline = self.analyzer.compute_similarity_timeline(
            self.term, 
            self.time_slices, 
            self.embedding_model
        )
        
        return [
            {"time_slice": ts, "similarity": sim}
            for ts, sim in timeline
        ]
    
    def export_results(self, output_path: str, shifts: List[ParadigmShift]) -> None:
        """
        Export detection results to JSON file.
        
        Args:
            output_path: Path to save results
            shifts: List of detected shifts
        """
        results = {
            "term": self.term,
            "time_slices": self.time_slices,
            "detected_shifts": [
                {
                    "year": s.year,
                    "similarity": s.similarity,
                    "significance_score": s.significance_score,
                    "context_before": s.context_before,
                    "context_after": s.context_after
                }
                for s in shifts
            ],
            "timeline": self.get_similarity_timeline()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        print(f"Results exported to {output_path}")
