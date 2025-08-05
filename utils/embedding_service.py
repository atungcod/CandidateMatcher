from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from typing import List, Union
import streamlit as st
import re

class EmbeddingService:
    """Service for generating embeddings from text using TF-IDF vectorization"""
    
    def __init__(self, max_features: int = 5000):
        """
        Initialize the embedding service
        
        Args:
            max_features: Maximum number of features for TF-IDF
        """
        self.max_features = max_features
        self.vectorizer = None
        self.is_fitted = False
        self._initialize_vectorizer()
    
    def _initialize_vectorizer(self):
        """Initialize the TF-IDF vectorizer"""
        try:
            self.vectorizer = TfidfVectorizer(
                max_features=self.max_features,
                stop_words='english',
                ngram_range=(1, 2),  # Use unigrams and bigrams
                lowercase=True,
                strip_accents='unicode'
            )
            self.is_fitted = False
        except Exception as e:
            raise Exception(f"Failed to initialize vectorizer: {str(e)}")
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text
        
        Args:
            text: Input text to generate embedding for
            
        Returns:
            np.ndarray: Embedding vector
            
        Raises:
            Exception: If embedding generation fails
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        try:
            # Preprocess text
            processed_text = self._preprocess_text(text)
            
            # If vectorizer is not fitted, fit it with this text
            if not self.is_fitted:
                self.vectorizer.fit([processed_text])
                self.is_fitted = True
            
            # Generate embedding using TF-IDF
            embedding = self.vectorizer.transform([processed_text]).toarray()[0]
            
            return embedding
            
        except Exception as e:
            raise Exception(f"Failed to generate embedding: {str(e)}")
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[np.ndarray]:
        """
        Generate embeddings for multiple texts in batch
        
        Args:
            texts: List of input texts
            
        Returns:
            List[np.ndarray]: List of embedding vectors
        """
        if not texts:
            return []
        
        try:
            # Preprocess all texts
            processed_texts = [self._preprocess_text(text) for text in texts]
            
            # Fit vectorizer with all texts if not fitted
            if not self.is_fitted:
                self.vectorizer.fit(processed_texts)
                self.is_fitted = True
            
            # Generate embeddings in batch (more efficient)
            embeddings_matrix = self.vectorizer.transform(processed_texts).toarray()
            
            # Convert to list of arrays
            return [embedding for embedding in embeddings_matrix]
            
        except Exception as e:
            raise Exception(f"Failed to generate batch embeddings: {str(e)}")
    
    def fit_vectorizer(self, texts: List[str]):
        """
        Fit the vectorizer with a corpus of texts
        
        Args:
            texts: List of texts to fit the vectorizer on
        """
        try:
            processed_texts = [self._preprocess_text(text) for text in texts]
            self.vectorizer.fit(processed_texts)
            self.is_fitted = True
        except Exception as e:
            raise Exception(f"Failed to fit vectorizer: {str(e)}")
    
    def _preprocess_text(self, text: str) -> str:
        """
        Preprocess text before embedding generation
        
        Args:
            text: Raw input text
            
        Returns:
            str: Preprocessed text
        """
        # Basic text preprocessing
        processed = text.strip()
        
        # Remove excessive whitespace
        processed = ' '.join(processed.split())
        
        # Truncate if too long (model limitations)
        max_length = 512  # Most sentence transformers have this limit
        if len(processed.split()) > max_length:
            processed = ' '.join(processed.split()[:max_length])
        
        return processed
    
    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of embeddings produced by this vectorizer
        
        Returns:
            int: Embedding dimension
        """
        try:
            if not self.is_fitted:
                # Fit with a test text to get dimension
                self.vectorizer.fit(["test text"])
                self.is_fitted = True
            return len(self.vectorizer.get_feature_names_out())
        except Exception as e:
            raise Exception(f"Failed to get embedding dimension: {str(e)}")
    
    def get_model_info(self) -> dict:
        """
        Get information about the vectorizer
        
        Returns:
            dict: Vectorizer information
        """
        return {
            'vectorizer_type': 'TF-IDF',
            'max_features': self.max_features,
            'embedding_dimension': self.get_embedding_dimension() if self.is_fitted else 'Not fitted yet',
            'is_fitted': self.is_fitted
        }
