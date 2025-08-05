# Job Candidate Recommendation System

## Overview

This is an AI-powered job candidate recommendation system built with Streamlit that helps recruiters find the best candidates for job positions. The system processes resumes in multiple formats (PDF, TXT, DOCX), generates embeddings using sentence transformers, calculates similarity scores between job descriptions and candidate resumes, and provides AI-generated summaries explaining why candidates are good fits for specific roles.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Streamlit Web Interface**: Simple, interactive web application with sidebar configuration options
- **File Upload System**: Supports multiple resume formats with drag-and-drop functionality
- **Results Display**: Shows ranked candidates with similarity scores and optional AI summaries
- **Caching Strategy**: Uses Streamlit's `@st.cache_resource` for service initialization to improve performance

### Backend Architecture
- **Modular Service Design**: Four main utility services handling distinct responsibilities
  - FileProcessor: Handles multi-format file processing (PDF, TXT, DOCX)
  - EmbeddingService: Generates vector embeddings using sentence transformers
  - SimilarityCalculator: Computes cosine similarity between job and resume embeddings
  - AISummarizer: Creates explanatory summaries using OpenAI's GPT models

### Data Processing Pipeline
- **Text Extraction**: Multi-format document processing with error handling
- **Embedding Generation**: Uses "all-MiniLM-L6-v2" sentence transformer model for semantic understanding
- **Similarity Scoring**: Cosine similarity calculation between job descriptions and resumes
- **AI Enhancement**: GPT-4o integration for generating human-readable candidate fit explanations

### Error Handling and Validation
- Comprehensive exception handling across all services
- Input validation for file formats and text content
- Graceful degradation when AI services are unavailable

## External Dependencies

### AI and ML Services
- **OpenAI API**: GPT-4o model for generating candidate fit summaries (requires OPENAI_API_KEY)
- **Sentence Transformers**: "all-MiniLM-L6-v2" model for semantic text embeddings
- **scikit-learn**: Cosine similarity calculations

### Document Processing Libraries
- **PyPDF2**: PDF text extraction
- **python-docx**: DOCX file processing
- **Built-in text processing**: For TXT files

### Web Framework and UI
- **Streamlit**: Complete web application framework with built-in caching and state management
- **pandas**: Data manipulation and display
- **numpy**: Numerical computations for embeddings and similarity scores

### Environment Configuration
- Requires `OPENAI_API_KEY` environment variable for AI summary generation
- All other dependencies are self-contained without external service requirements