import streamlit as st
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
import os
from utils.file_processor import FileProcessor
from utils.embedding_service import EmbeddingService
from utils.similarity_calculator import SimilarityCalculator
from utils.ai_summarizer import AISummarizer

# Configure Streamlit page
st.set_page_config(
    page_title="Job Candidate Recommendation System",
    page_icon="🎯",
    layout="wide"
)

# Initialize services
@st.cache_resource
def initialize_services():
    """Initialize all services with caching for better performance"""
    file_processor = FileProcessor()
    embedding_service = EmbeddingService()
    similarity_calculator = SimilarityCalculator()
    ai_summarizer = AISummarizer()
    return file_processor, embedding_service, similarity_calculator, ai_summarizer

def main():
    st.title("🎯 Job Candidate Recommendation System")
    st.markdown("Find the best candidates for your job using AI-powered matching")
    
    # Initialize services
    try:
        file_processor, embedding_service, similarity_calculator, ai_summarizer = initialize_services()
    except Exception as e:
        st.error(f"Failed to initialize services: {str(e)}")
        st.stop()
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        num_candidates = st.slider(
            "Number of top candidates to show",
            min_value=5,
            max_value=10,
            value=10,
            help="Select how many top candidates to display"
        )
        
        # Check if AI summarizer is available
        ai_available = ai_summarizer.is_available
        provider_info = ai_summarizer.get_provider_info()
        
        if ai_available:
            generate_summaries = st.checkbox(
                "Generate AI summaries",
                value=True,
                help=f"Generate AI-powered explanations using {provider_info['provider'].title()} {provider_info['model']}"
            )
            st.info(f"🤖 AI Provider: {provider_info['provider'].title()} ({provider_info['model']})")
        else:
            generate_summaries = st.checkbox(
                "Generate AI summaries",
                value=False,
                disabled=True,
                help="AI API key required for summaries"
            )
            st.warning("💡 **Enable AI Summaries:**\n\n"
                      "Add one of these API keys:\n"
                      "• **GEMINI_API_KEY** (Google Gemini - has free tier)\n"
                      "• **ANTHROPIC_API_KEY** (Anthropic Claude)\n" 
                      "• **OPENAI_API_KEY** (OpenAI GPT)")
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📋 Job Description")
        job_description = st.text_area(
            "Enter the job description:",
            height=300,
            placeholder="Paste your job description here...",
            help="Provide a detailed job description including requirements, responsibilities, and qualifications"
        )
    
    with col2:
        st.header("📄 Candidate Resumes")
        
        # Choose input method
        input_method = st.radio(
            "How would you like to provide resumes?",
            ["Upload Files", "Text Input"],
            horizontal=True
        )
        
        resumes_data = []
        
        if input_method == "Upload Files":
            uploaded_files = st.file_uploader(
                "Upload resume files",
                type=['pdf', 'txt', 'docx'],
                accept_multiple_files=True,
                help="Supported formats: PDF, TXT, DOCX"
            )
            
            if uploaded_files:
                with st.spinner("Processing uploaded files..."):
                    for uploaded_file in uploaded_files:
                        try:
                            content = file_processor.process_file(uploaded_file)
                            if content.strip():
                                resumes_data.append({
                                    'name': uploaded_file.name,
                                    'content': content
                                })
                        except Exception as e:
                            st.error(f"Error processing {uploaded_file.name}: {str(e)}")
                
                if resumes_data:
                    st.success(f"Successfully processed {len(resumes_data)} resume(s)")
        
        else:  # Text Input
            st.markdown("**Enter resumes as text (one per text area):**")
            
            # Dynamic text areas for resumes
            if 'num_text_resumes' not in st.session_state:
                st.session_state.num_text_resumes = 3
            
            col_a, col_b = st.columns([3, 1])
            with col_a:
                num_text_areas = st.number_input(
                    "Number of resumes",
                    min_value=1,
                    max_value=20,
                    value=st.session_state.num_text_resumes
                )
            with col_b:
                if st.button("Update"):
                    st.session_state.num_text_resumes = num_text_areas
                    st.rerun()
            
            for i in range(st.session_state.num_text_resumes):
                resume_text = st.text_area(
                    f"Resume {i+1}:",
                    height=150,
                    key=f"resume_text_{i}",
                    placeholder=f"Paste resume {i+1} content here..."
                )
                
                if resume_text.strip():
                    resumes_data.append({
                        'name': f"Candidate {i+1}",
                        'content': resume_text.strip()
                    })
    
    # Process and display results
    if st.button("🔍 Find Best Candidates", type="primary", use_container_width=True):
        if not job_description.strip():
            st.error("Please enter a job description")
            return
        
        if not resumes_data:
            st.error("Please provide at least one resume")
            return
        
        try:
            with st.spinner("Analyzing candidates... This may take a moment"):
                # Generate embeddings
                progress_bar = st.progress(0, text="Preparing text analysis...")
                
                # Prepare all texts for fitting the vectorizer
                all_texts = [job_description] + [resume['content'] for resume in resumes_data]
                
                # Fit the vectorizer with all texts for better vocabulary
                progress_bar.progress(25, text="Training text analyzer...")
                embedding_service.fit_vectorizer(all_texts)
                
                # Generate job embedding
                progress_bar.progress(40, text="Analyzing job description...")
                job_embedding = embedding_service.generate_embedding(job_description)
                
                # Generate resume embeddings
                progress_bar.progress(50, text="Analyzing resumes...")
                resume_texts = [resume['content'] for resume in resumes_data]
                resume_embeddings = embedding_service.generate_embeddings_batch(resume_texts)
                
                # Calculate similarities
                progress_bar.progress(75, text="Calculating similarities...")
                similarities = similarity_calculator.calculate_similarities(
                    job_embedding, 
                    resume_embeddings
                )
                
                # Combine data and sort by similarity
                candidates_with_scores = []
                for i, (resume, similarity) in enumerate(zip(resumes_data, similarities)):
                    candidates_with_scores.append({
                        'name': resume['name'],
                        'content': resume['content'],
                        'similarity': similarity,
                        'rank': i + 1
                    })
                
                # Sort by similarity (descending)
                candidates_with_scores.sort(key=lambda x: x['similarity'], reverse=True)
                
                # Take top N candidates
                top_candidates = candidates_with_scores[:num_candidates]
                
                progress_bar.progress(100, text="Analysis complete!")
                progress_bar.empty()
                
                # Display results
                st.header("🏆 Top Candidates")
                
                for i, candidate in enumerate(top_candidates):
                    with st.expander(
                        f"#{i+1} - {candidate['name']} (Similarity: {candidate['similarity']:.2%})",
                        expanded=(i < 3)  # Expand top 3 by default
                    ):
                        col_left, col_right = st.columns([2, 1])
                        
                        with col_left:
                            st.subheader("Resume Content")
                            st.text_area(
                                "Content:",
                                value=candidate['content'][:1000] + ("..." if len(candidate['content']) > 1000 else ""),
                                height=200,
                                disabled=True,
                                key=f"content_{i}"
                            )
                        
                        with col_right:
                            st.subheader("Match Score")
                            # Create a visual score representation
                            score_percentage = candidate['similarity'] * 100
                            st.metric(
                                label="Similarity Score",
                                value=f"{score_percentage:.1f}%",
                                delta=f"Rank #{i+1}"
                            )
                            
                            # Score bar visualization
                            progress_color = "🟩" if score_percentage >= 70 else "🟨" if score_percentage >= 50 else "🟥"
                            st.write(f"Match Quality: {progress_color}")
                        
                        # Generate AI summary if enabled
                        if generate_summaries:
                            with st.spinner(f"Generating AI summary for {candidate['name']}..."):
                                try:
                                    summary = ai_summarizer.generate_fit_summary(
                                        job_description, 
                                        candidate['content'],
                                        candidate['similarity']
                                    )
                                    
                                    st.subheader("🤖 AI Analysis")
                                    st.info(summary)
                                    
                                except Exception as e:
                                    st.warning(f"Could not generate AI summary: {str(e)}")
                
                # Summary statistics
                st.header("📊 Analysis Summary")
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                
                with col_stat1:
                    st.metric(
                        "Total Candidates Analyzed",
                        len(resumes_data)
                    )
                
                with col_stat2:
                    avg_similarity = np.mean([c['similarity'] for c in top_candidates])
                    st.metric(
                        "Average Similarity (Top Candidates)",
                        f"{avg_similarity:.1%}"
                    )
                
                with col_stat3:
                    best_match = top_candidates[0]['similarity'] if top_candidates else 0
                    st.metric(
                        "Best Match Score",
                        f"{best_match:.1%}"
                    )
                
                # Download results option
                if st.button("📥 Download Results as CSV"):
                    results_df = pd.DataFrame([
                        {
                            'Rank': i + 1,
                            'Candidate': candidate['name'],
                            'Similarity_Score': f"{candidate['similarity']:.4f}",
                            'Similarity_Percentage': f"{candidate['similarity']:.2%}"
                        }
                        for i, candidate in enumerate(top_candidates)
                    ])
                    
                    csv = results_df.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name="candidate_recommendations.csv",
                        mime="text/csv"
                    )
        
        except Exception as e:
            st.error(f"An error occurred during analysis: {str(e)}")
            st.exception(e)

if __name__ == "__main__":
    main()
