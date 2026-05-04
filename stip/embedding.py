"""
Temporal embedding module for building word embeddings per time slice.
"""

import numpy as np
from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import CountVectorizer
from scipy.sparse import csr_matrix


class TemporalEmbedding:
    """
    Builds and manages word embeddings for different time slices.
    
    This class creates vector representations of terms within specific
    time periods to track semantic changes over time.
    """
    
    def __init__(self, embedding_dim: int = 300, window_size: int = 5):
        """
        Initialize the temporal embedding generator.
        
        Args:
            embedding_dim: Dimension of the embedding vectors
            window_size: Context window size for extracting co-occurrences
        """
        self.embedding_dim = embedding_dim
        self.window_size = window_size
        self.time_slice_embeddings: Dict[str, np.ndarray] = {}
        self.vocabulary: Dict[str, int] = {}
        self.reverse_vocabulary: Dict[int, str] = {}
        
    def build_co_occurrence_matrix(self, documents: List[str], 
                                    time_slice: str) -> csr_matrix:
        """
        Build a co-occurrence matrix from documents in a time slice.
        
        Args:
            documents: List of text documents (abstracts)
            time_slice: Identifier for the time period
            
        Returns:
            Sparse co-occurrence matrix
        """
        # Use lower min_df and remove max_df to handle small/homogeneous datasets
        vectorizer = CountVectorizer(min_df=1, max_features=1000)
        term_doc_matrix = vectorizer.fit_transform(documents)
        
        # Update vocabulary
        self.vocabulary = vectorizer.vocabulary_
        self.reverse_vocabulary = {v: k for v, k in self.vocabulary.items()}
        
        # Compute co-occurrence (term-document-term)
        co_occurrence = term_doc_matrix.T @ term_doc_matrix
        
        return co_occurrence
    
    def create_embeddings(self, co_occurrence_matrix: csr_matrix, 
                          method: str = 'svd') -> np.ndarray:
        """
        Create embeddings from co-occurrence matrix using SVD or other methods.
        
        Args:
            co_occurrence_matrix: The co-occurrence matrix
            method: Method for creating embeddings ('svd', 'ppmi')
            
        Returns:
            Embedding matrix of shape (vocab_size, embedding_dim)
        """
        if method == 'svd':
            from scipy.sparse.linalg import svds
            
            # Truncated SVD for dimensionality reduction
            k = min(self.embedding_dim, co_occurrence_matrix.shape[0] - 1)
            U, S, Vt = svds(co_occurrence_matrix.astype(float), k=k)
            
            # Weight by singular values
            embeddings = U @ np.diag(np.sqrt(S))
            
            # Pad if necessary
            if embeddings.shape[1] < self.embedding_dim:
                padding = np.zeros((embeddings.shape[0], 
                                   self.embedding_dim - embeddings.shape[1]))
                embeddings = np.hstack([embeddings, padding])
                
            return embeddings
        else:
            raise ValueError(f"Unknown method: {method}")
    
    def fit_time_slice(self, documents: List[str], time_slice: str, 
                       method: str = 'svd') -> np.ndarray:
        """
        Fit embeddings for a specific time slice.
        
        Args:
            documents: List of documents from this time period
            time_slice: Time period identifier (e.g., "1990-1995")
            method: Embedding method
            
        Returns:
            Embedding matrix for this time slice
        """
        co_occurrence = self.build_co_occurrence_matrix(documents, time_slice)
        embeddings = self.create_embeddings(co_occurrence, method)
        
        self.time_slice_embeddings[time_slice] = embeddings
        return embeddings
    
    def get_term_vector(self, term: str, time_slice: str) -> np.ndarray:
        """
        Get the embedding vector for a term in a specific time slice.
        
        Args:
            term: The term to look up
            time_slice: Time period identifier
            
        Returns:
            Embedding vector or None if term not found
        """
        if time_slice not in self.time_slice_embeddings:
            return None
            
        if term not in self.vocabulary:
            return None
            
        idx = self.vocabulary[term]
        embeddings = self.time_slice_embeddings[time_slice]
        
        if idx >= embeddings.shape[0]:
            return None
            
        return embeddings[idx]
    
    def compute_similarity(self, term: str, time_slice1: str, 
                          time_slice2: str) -> float:
        """
        Compute cosine similarity of a term between two time slices.
        
        Args:
            term: The term to compare
            time_slice1: First time period
            time_slice2: Second time period
            
        Returns:
            Cosine similarity score (0.0 to 1.0)
        """
        vec1 = self.get_term_vector(term, time_slice1)
        vec2 = self.get_term_vector(term, time_slice2)
        
        if vec1 is None or vec2 is None:
            return 0.0
        
        # Compute cosine similarity
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        similarity = np.dot(vec1, vec2) / (norm1 * norm2)
        return float(similarity)
