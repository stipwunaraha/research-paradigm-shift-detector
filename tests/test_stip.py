"""
Tests for the STIP paradigm shift detection module.
"""

import pytest
import json
import os
import tempfile
from pathlib import Path

from stip.embedding import TemporalEmbedding
from stip.shift_analyzer import ShiftAnalyzer, ParadigmShift
from stip.detector import ParadigmShiftDetector


class TestTemporalEmbedding:
    """Tests for TemporalEmbedding class."""
    
    def test_initialization(self):
        """Test that TemporalEmbedding initializes correctly."""
        embedding = TemporalEmbedding(embedding_dim=100, window_size=3)
        assert embedding.embedding_dim == 100
        assert embedding.window_size == 3
        assert len(embedding.time_slice_embeddings) == 0
    
    def test_fit_time_slice(self):
        """Test fitting embeddings for a time slice."""
        embedding = TemporalEmbedding(embedding_dim=50)
        
        documents = [
            "Machine learning is a subset of artificial intelligence.",
            "Deep learning uses neural networks with many layers.",
            "Natural language processing enables computers to understand text.",
        ] * 5  # Repeat to ensure enough data
        
        embeddings = embedding.fit_time_slice(documents, "2015-2020")
        
        assert "2015-2020" in embedding.time_slice_embeddings
        assert embeddings.shape[1] == 50
    
    def test_compute_similarity(self):
        """Test similarity computation between time slices."""
        embedding = TemporalEmbedding(embedding_dim=50)
        
        # Create two similar time slices with enough repeated terms
        docs1 = [
            "artificial intelligence and machine learning algorithms",
            "machine learning and deep neural networks",
            "artificial intelligence research and development",
            "neural networks for pattern recognition",
            "machine learning applications in science",
        ] * 5
        docs2 = [
            "artificial intelligence and machine learning systems",
            "machine learning and artificial neural networks", 
            "artificial intelligence in modern computing",
            "deep learning and neural architectures",
            "machine learning for data analysis",
        ] * 5
        
        embedding.fit_time_slice(docs1, "2000-2005")
        embedding.fit_time_slice(docs2, "2005-2010")
        
        # Test similarity for a term that should exist
        similarity = embedding.compute_similarity("learning", "2000-2005", "2005-2010")
        assert -1.0 <= similarity <= 1.0


class TestShiftAnalyzer:
    """Tests for ShiftAnalyzer class."""
    
    def test_initialization(self):
        """Test that ShiftAnalyzer initializes correctly."""
        analyzer = ShiftAnalyzer(threshold=0.4, significance_level=0.01)
        assert analyzer.threshold == 0.4
        assert analyzer.significance_level == 0.01
    
    def test_detect_drops(self):
        """Test detection of similarity drops."""
        analyzer = ShiftAnalyzer(threshold=0.5)
        
        timeline = [
            ("1990-1995", 0.9),
            ("1995-2000", 0.85),
            ("2000-2005", 0.3),  # Significant drop
            ("2005-2010", 0.25),  # Another low value
        ]
        
        shifts = analyzer.detect_drops(timeline, "test_term")
        
        assert len(shifts) >= 1
        assert all(s.similarity < 0.5 for s in shifts)


class TestParadigmShiftDetector:
    """Tests for ParadigmShiftDetector class."""
    
    @pytest.fixture
    def sample_corpus_file(self):
        """Create a temporary sample corpus file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            # Write sample documents
            for year in range(1990, 2010):
                doc = {
                    "year": year,
                    "title": f"Paper {year}",
                    "abstract": "This is a test abstract about machine learning."
                }
                f.write(json.dumps(doc) + '\n')
            
            temp_path = f.name
        
        yield temp_path
        
        # Cleanup
        os.unlink(temp_path)
    
    def test_initialization(self, sample_corpus_file):
        """Test that ParadigmShiftDetector initializes correctly."""
        detector = ParadigmShiftDetector(
            corpus_path=sample_corpus_file,
            term="learning",
            time_slice_years=5
        )
        
        assert detector.term == "learning"
        assert detector.time_slice_years == 5
    
    def test_load_corpus(self, sample_corpus_file):
        """Test corpus loading."""
        detector = ParadigmShiftDetector(
            corpus_path=sample_corpus_file,
            term="learning"
        )
        
        detector.load_corpus()
        
        assert len(detector.time_slices) > 0
        assert len(detector.documents_by_slice) > 0
    
    def test_detect_shifts(self, sample_corpus_file):
        """Test shift detection pipeline."""
        detector = ParadigmShiftDetector(
            corpus_path=sample_corpus_file,
            term="learning",
            threshold=0.1  # Low threshold to detect shifts easily
        )
        
        shifts = detector.detect_shifts()
        
        # Should return a list (may be empty if no significant shifts)
        assert isinstance(shifts, list)


class TestIntegration:
    """Integration tests for the full pipeline."""
    
    def test_full_pipeline(self):
        """Test the complete paradigm shift detection pipeline."""
        # Create temporary corpus
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            # Pre-shift era
            for year in range(1990, 2000):
                for _ in range(20):
                    doc = {
                        "year": year,
                        "title": "Cognitive study",
                        "abstract": "Human attention and perception in visual tasks."
                    }
                    f.write(json.dumps(doc) + '\n')
            
            # Post-shift era with more varied vocabulary
            for year in range(2000, 2010):
                for _ in range(20):
                    doc = {
                        "year": year,
                        "title": "ML paper",
                        "abstract": "Attention mechanisms and transformer neural networks for deep learning and natural language processing tasks."
                    }
                    f.write(json.dumps(doc) + '\n')
            
            temp_path = f.name
        
        try:
            # Run full pipeline
            detector = ParadigmShiftDetector(
                corpus_path=temp_path,
                term="attention",
                time_slice_years=5,
                threshold=0.3
            )
            
            detector.load_corpus()
            detector.build_embeddings()
            shifts = detector.detect_shifts()
            
            # Verify results structure
            assert isinstance(shifts, list)
            
        finally:
            os.unlink(temp_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
