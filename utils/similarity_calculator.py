import numpy as np
from typing import List, Union
from sklearn.metrics.pairwise import cosine_similarity

class SimilarityCalculator:
    """Calculate similarity scores between embeddings"""
    
    def __init__(self):
        """Initialize the similarity calculator"""
        pass
    
    def calculate_similarities(
        self, 
        job_embedding: np.ndarray, 
        resume_embeddings: List[np.ndarray]
    ) -> List[float]:
        """
        Calculate cosine similarities between job embedding and resume embeddings
        
        Args:
            job_embedding: Embedding vector for the job description
            resume_embeddings: List of embedding vectors for resumes
            
        Returns:
            List[float]: List of similarity scores (0-1 range)
            
        Raises:
            Exception: If similarity calculation fails
        """
        if job_embedding is None or len(resume_embeddings) == 0:
            raise ValueError("Job embedding and resume embeddings cannot be empty")
        
        try:
            # Ensure job embedding is 2D for sklearn
            if job_embedding.ndim == 1:
                job_embedding = job_embedding.reshape(1, -1)
            
            # Convert resume embeddings to 2D array
            resume_matrix = np.vstack(resume_embeddings)
            
            # Calculate cosine similarities
            similarities = cosine_similarity(job_embedding, resume_matrix)[0]
            
            # Ensure all similarities are between 0 and 1
            similarities = np.clip(similarities, 0, 1)
            
            return similarities.tolist()
            
        except Exception as e:
            raise Exception(f"Failed to calculate similarities: {str(e)}")
    
    def calculate_pairwise_similarities(
        self, 
        embeddings: List[np.ndarray]
    ) -> np.ndarray:
        """
        Calculate pairwise similarities between all embeddings
        
        Args:
            embeddings: List of embedding vectors
            
        Returns:
            np.ndarray: Matrix of pairwise similarities
        """
        if len(embeddings) < 2:
            raise ValueError("Need at least 2 embeddings for pairwise calculation")
        
        try:
            # Convert to matrix
            embedding_matrix = np.vstack(embeddings)
            
            # Calculate pairwise cosine similarities
            similarity_matrix = cosine_similarity(embedding_matrix)
            
            return similarity_matrix
            
        except Exception as e:
            raise Exception(f"Failed to calculate pairwise similarities: {str(e)}")
    
    def get_top_matches(
        self, 
        similarities: List[float], 
        top_k: int = 10
    ) -> List[tuple]:
        """
        Get indices and scores of top K matches
        
        Args:
            similarities: List of similarity scores
            top_k: Number of top matches to return
            
        Returns:
            List[tuple]: List of (index, similarity_score) tuples, sorted by score
        """
        if not similarities:
            return []
        
        # Create list of (index, score) tuples
        indexed_similarities = [(i, score) for i, score in enumerate(similarities)]
        
        # Sort by similarity score (descending)
        sorted_similarities = sorted(indexed_similarities, key=lambda x: x[1], reverse=True)
        
        # Return top K
        return sorted_similarities[:top_k]
    
    def calculate_similarity_statistics(self, similarities: List[float]) -> dict:
        """
        Calculate statistics for similarity scores
        
        Args:
            similarities: List of similarity scores
            
        Returns:
            dict: Statistics including mean, std, min, max, etc.
        """
        if not similarities:
            return {}
        
        similarities_array = np.array(similarities)
        
        return {
            'mean': float(np.mean(similarities_array)),
            'std': float(np.std(similarities_array)),
            'min': float(np.min(similarities_array)),
            'max': float(np.max(similarities_array)),
            'median': float(np.median(similarities_array)),
            'count': len(similarities),
            'above_70_percent': int(np.sum(similarities_array > 0.7)),
            'above_50_percent': int(np.sum(similarities_array > 0.5)),
            'above_30_percent': int(np.sum(similarities_array > 0.3))
        }
    
    @staticmethod
    def normalize_similarities(similarities: List[float]) -> List[float]:
        """
        Normalize similarity scores to 0-1 range using min-max normalization
        
        Args:
            similarities: List of similarity scores
            
        Returns:
            List[float]: Normalized similarity scores
        """
        if not similarities:
            return []
        
        similarities_array = np.array(similarities)
        
        min_sim = np.min(similarities_array)
        max_sim = np.max(similarities_array)
        
        # Avoid division by zero
        if max_sim == min_sim:
            return [0.5] * len(similarities)
        
        normalized = (similarities_array - min_sim) / (max_sim - min_sim)
        
        return normalized.tolist()
    
    @staticmethod
    def get_similarity_category(similarity_score: float) -> str:
        """
        Categorize similarity score into human-readable categories
        
        Args:
            similarity_score: Similarity score between 0 and 1
            
        Returns:
            str: Category description
        """
        if similarity_score >= 0.8:
            return "Excellent Match"
        elif similarity_score >= 0.7:
            return "Very Good Match"
        elif similarity_score >= 0.6:
            return "Good Match"
        elif similarity_score >= 0.5:
            return "Moderate Match"
        elif similarity_score >= 0.3:
            return "Weak Match"
        else:
            return "Poor Match"
