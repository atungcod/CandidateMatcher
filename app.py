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
st.set_page_config(page_title="Job Candidate Recommendation System",
                   page_icon="🎯",
                   layout="wide")

# Initialize session state for navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'search'
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None


# Initialize services
@st.cache_resource
def initialize_services():
    """Initialize all services with caching for better performance"""
    file_processor = FileProcessor()
    embedding_service = EmbeddingService()
    similarity_calculator = SimilarityCalculator()
    ai_summarizer = AISummarizer()
    return file_processor, embedding_service, similarity_calculator, ai_summarizer


def show_search_page():
    """Display the search/input page"""
    # Enhanced CSS styling for modern UI
    st.markdown("""
    <style>
    /* Global styling improvements */
    .main > div {
        padding-top: 1rem;
    }
    
    /* Hero section with animated gradient */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shimmer 4s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .hero-section h1 {
        color: white;
        font-size: 3rem;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .hero-section p {
        color: rgba(255,255,255,0.9);
        font-size: 1.3rem;
        margin: 1rem 0 0 0;
        position: relative;
        z-index: 1;
    }
    
    /* Feature showcase with glassmorphism */
    .feature-showcase {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 2rem;
        border-radius: 16px;
        margin: 2rem 0;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin-top: 1rem;
    }
    
    .feature-item {
        text-align: center;
        padding: 1rem;
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .feature-item h4 {
        color: #667eea;
        margin: 0;
        font-size: 1.1rem;
    }
    
    .feature-item p {
        margin: 0.5rem 0 0 0;
        font-size: 0.9rem;
        color: #666;
    }
    
    /* Enhanced input sections */
    .input-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .input-section {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border: 1px solid rgba(0,0,0,0.05);
        position: relative;
        overflow: hidden;
    }
    
    .input-section:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.15);
    }
    
    .job-section {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
    }
    
    .upload-section {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    }
    
    .input-section h2 {
        margin-top: 0;
        color: #333;
        font-size: 1.5rem;
    }
    
    /* Enhanced CTA button */
    .cta-container {
        text-align: center;
        margin: 3rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        padding: 1rem 3rem !important;
        border-radius: 50px !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.6) !important;
        background: linear-gradient(45deg, #5a67d8, #6b46c1) !important;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* Sidebar enhancements */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
        border-right: 1px solid #dee2e6;
    }
    
    .css-1d391kg .css-1v3fvcr {
        background: white;
        border-radius: 8px;
        margin: 0.5rem 0;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .hero-section h1 {
            font-size: 2rem;
        }
        
        .hero-section p {
            font-size: 1.1rem;
        }
        
        .input-container {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
        
        .feature-grid {
            grid-template-columns: repeat(2, 1fr);
        }
        
        .input-section {
            padding: 1.5rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Enhanced hero section
    st.markdown("""
    <div class="hero-section">
        <h1>🎯 Smart Candidate Matching</h1>
        <p>AI-powered recruitment made simple, fast, and incredibly effective</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature showcase
    st.markdown("""
    <div class="feature-showcase">
        <h3 style="text-align: center; margin-top: 0; color: #333;">Why Choose Smart Matching?</h3>
        <div class="feature-grid">
            <div class="feature-item">
                <span class="feature-icon">⚡</span>
                <h4>Lightning Fast</h4>
                <p>Seconds not hours</p>
            </div>
            <div class="feature-item">
                <span class="feature-icon">🎯</span>
                <h4>Precise Matching</h4>
                <p>AI-powered accuracy</p>
            </div>
            <div class="feature-item">
                <span class="feature-icon">💡</span>
                <h4>Smart Insights</h4>
                <p>Detailed explanations</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Initialize services
    try:
        file_processor, embedding_service, similarity_calculator, ai_summarizer = initialize_services(
        )
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
            help="Select how many top candidates to display")

        # Check if AI summarizer is available
        ai_available = ai_summarizer.is_available
        provider_info = ai_summarizer.get_provider_info()
        API_KEY = "AIzaSyA8IiyUq0iH-1ZYY4hVWPL_csk4GbYK4BY"

        if ai_available:
            generate_summaries = st.checkbox(
                "Generate AI summaries",
                value=True,
                help=
                f"Generate AI-powered explanations using {provider_info['provider'].title()} {provider_info['model']}"
            )
            st.info(
                f"🤖 AI Provider: {provider_info['provider'].title()} ({provider_info['model']})"
            )
        else:
            generate_summaries = st.checkbox(
                "Generate AI summaries",
                value=False,
                disabled=True,
                help="AI API key required for summaries")

    # Enhanced main content area with styled containers
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="input-section job-section">', unsafe_allow_html=True)
        st.header("📋 Job Description")
        job_description = st.text_area(
            "Enter the job description:",
            height=300,
            placeholder="Describe the ideal candidate, required skills, experience, and key responsibilities...",
            help="💡 Tip: Include specific skills, experience levels, and key responsibilities for better matching"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="input-section upload-section">', unsafe_allow_html=True)
        st.header("📄 Candidate Resumes")

        # Enhanced input method selection
        st.markdown("**Choose how to provide resumes:**")
        input_method = st.radio("Resume Input Method",
                                ["📁 Upload Files", "✏️ Text Input"],
                                horizontal=True,
                                help="Upload files or paste resume text directly",
                                label_visibility="collapsed")

        resumes_data = []

        if input_method == "📁 Upload Files":
            st.markdown("**Drag and drop your files or click to browse:**")
            uploaded_files = st.file_uploader(
                "Upload resume files",
                type=['pdf', 'txt', 'docx'],
                accept_multiple_files=True,
                help="✅ Supported formats: PDF, TXT, DOCX | 📁 Multiple files allowed")

            if uploaded_files:
                with st.spinner("🔄 Processing uploaded files..."):
                    progress_text = st.empty()
                    for i, uploaded_file in enumerate(uploaded_files):
                        progress_text.text(f"Processing {uploaded_file.name}...")
                        try:
                            content = file_processor.process_file(uploaded_file)
                            if content.strip():
                                resumes_data.append({
                                    'name': uploaded_file.name,
                                    'content': content
                                })
                        except Exception as e:
                            st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
                    
                    progress_text.empty()

                if resumes_data:
                    st.success(f"✅ Successfully processed {len(resumes_data)} resume(s)")

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
                    value=st.session_state.num_text_resumes)
            with col_b:
                if st.button("🔄 Update"):
                    st.session_state.num_text_resumes = num_text_areas
                    st.rerun()

            for i in range(st.session_state.num_text_resumes):
                resume_text = st.text_area(
                    f"📝 Resume {i+1}:",
                    height=150,
                    key=f"resume_text_{i}",
                    placeholder=f"Paste the full resume content for candidate {i+1} here...")

                if resume_text.strip():
                    resumes_data.append({
                        'name': f"Candidate {i+1}",
                        'content': resume_text.strip()
                    })
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close upload section
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close input container

    # Enhanced CTA section with container
    st.markdown('<div class="cta-container">', unsafe_allow_html=True)
    
    # Display resume count if available
    if resumes_data:
        st.info(f"📊 Ready to analyze {len(resumes_data)} candidate(s)")
    
    # Process and analyze candidates
    if st.button("🚀 Find Best Candidates",
                 type="primary",
                 use_container_width=True):
        if not job_description.strip():
            st.error("❌ Please enter a job description with specific requirements and responsibilities")
            st.markdown('</div>', unsafe_allow_html=True)
            return

        if not resumes_data:
            st.error("❌ Please provide at least one resume to analyze")
            st.markdown('</div>', unsafe_allow_html=True)
            return

        try:
            with st.spinner("Analyzing candidates... This may take a moment"):
                # Generate embeddings
                progress_bar = st.progress(0,
                                           text="Preparing text analysis...")

                # Prepare all texts for fitting the vectorizer
                all_texts = [job_description] + [
                    resume['content'] for resume in resumes_data
                ]

                # Fit the vectorizer with all texts for better vocabulary
                progress_bar.progress(25, text="Training text analyzer...")
                embedding_service.fit_vectorizer(all_texts)

                # Generate job embedding
                progress_bar.progress(40, text="Analyzing job description...")
                job_embedding = embedding_service.generate_embedding(
                    job_description)

                # Generate resume embeddings
                progress_bar.progress(50, text="Analyzing resumes...")
                resume_texts = [resume['content'] for resume in resumes_data]
                resume_embeddings = embedding_service.generate_embeddings_batch(
                    resume_texts)

                # Calculate similarities
                progress_bar.progress(75, text="Calculating similarities...")
                similarities = similarity_calculator.calculate_similarities(
                    job_embedding, resume_embeddings)

                # Combine data and sort by similarity
                candidates_with_scores = []
                for i, (resume, similarity) in enumerate(
                        zip(resumes_data, similarities)):
                    candidates_with_scores.append({
                        'name': resume['name'],
                        'content': resume['content'],
                        'similarity': similarity,
                        'rank': i + 1
                    })

                # Sort by similarity (descending)
                candidates_with_scores.sort(key=lambda x: x['similarity'],
                                            reverse=True)

                # Take top N candidates
                top_candidates = candidates_with_scores[:num_candidates]

                progress_bar.progress(100, text="Analysis complete!")
                progress_bar.empty()

                # Store results in session state and navigate to results page
                st.session_state.analysis_results = {
                    'job_description': job_description,
                    'top_candidates': top_candidates,
                    'total_candidates': len(resumes_data),
                    'generate_summaries': generate_summaries,
                    'ai_summarizer': ai_summarizer
                }
                st.session_state.current_page = 'results'
                st.rerun()

        except Exception as e:
            st.error(f"❌ An error occurred during analysis: {str(e)}")
            st.exception(e)
        finally:
            st.markdown('</div>', unsafe_allow_html=True)  # Close CTA container
    
    else:
        st.markdown('</div>', unsafe_allow_html=True)  # Close CTA container


def show_results_page():
    """Display the enhanced results page with candidate rankings"""
    # Enhanced CSS for modern results page
    st.markdown("""
    <style>
    /* Results page styling */
    .results-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
    }
    
    .results-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shimmer 4s infinite;
    }
    
    .results-content {
        position: relative;
        z-index: 1;
    }
    
    .results-title {
        margin: 0;
        font-size: 2.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .results-subtitle {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Enhanced stats grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: white;
        padding: 2rem 1.5rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border-top: 4px solid #667eea;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.15);
    }
    
    .stat-card:nth-child(2) {
        border-top-color: #28a745;
    }
    
    .stat-card:nth-child(3) {
        border-top-color: #ffc107;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: #667eea;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .stat-label {
        color: #6c757d;
        font-size: 1rem;
        font-weight: 500;
    }
    
    /* Enhanced buttons */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 25px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5) !important;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .results-header {
            padding: 2rem 1rem;
        }
        
        .results-title {
            font-size: 2rem;
        }
        
        .stats-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    results = st.session_state.analysis_results

    if not results:
        st.error("❌ No analysis results found. Please go back and run an analysis first.")
        if st.button("← Back to Search"):
            st.session_state.current_page = 'search'
            st.rerun()
        return

    # Enhanced header with modern styling
    st.markdown(f"""
    <div class="results-header">
        <div class="results-content">
            <h1 class="results-title">🏆 Top Candidates Found</h1>
            <p class="results-subtitle">Analysis completed for: {results['job_description'][:80]}{'...' if len(results['job_description']) > 80 else ''}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Back navigation button
    if st.button("← Back to Search", key="back_to_search"):
        st.session_state.current_page = 'search'
        st.rerun()

    # Enhanced summary statistics with modern cards
    st.markdown("""
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-number">{}</div>
            <div class="stat-label">Total Candidates</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{:.0%}</div>
            <div class="stat-label">Average Match</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{:.0%}</div>
            <div class="stat-label">Best Match</div>
        </div>
    </div>
    """.format(
        results['total_candidates'],
        np.mean([c['similarity'] for c in results['top_candidates']]) if results['top_candidates'] else 0,
        results['top_candidates'][0]['similarity'] if results['top_candidates'] else 0
    ), unsafe_allow_html=True)

    # Enhanced candidate display section
    st.markdown("---")
    
    for i, candidate in enumerate(results['top_candidates']):
        # Determine score styling
        score_percentage = candidate['similarity'] * 100
        if score_percentage >= 80:
            score_class = "excellent"
            score_color = "#4facfe"
            score_emoji = "🏆"
        elif score_percentage >= 60:
            score_class = "good" 
            score_color = "#43e97b"
            score_emoji = "⭐"
        else:
            score_class = "fair"
            score_color = "#fa709a"
            score_emoji = "📋"
        
        # Enhanced candidate card
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 16px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            margin: 1.5rem 0;
            overflow: hidden;
            border-left: 4px solid {score_color};
            transition: all 0.3s ease;
        ">
            <div style="
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                padding: 2rem;
                border-bottom: 1px solid rgba(0,0,0,0.05);
                display: flex;
                justify-content: space-between;
                align-items: center;
            ">
                <div>
                    <h3 style="margin: 0; color: #333; font-size: 1.5rem;">
                        {score_emoji} #{i+1} - {candidate['name']}
                    </h3>
                    <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 1rem;">
                        Match Analysis Complete
                    </p>
                </div>
                <div style="
                    background: linear-gradient(135deg, {score_color}, {score_color}99);
                    color: white;
                    padding: 0.75rem 1.5rem;
                    border-radius: 25px;
                    font-weight: bold;
                    font-size: 1.1rem;
                    box-shadow: 0 4px 15px {score_color}33;
                ">
                    {score_percentage:.1f}% Match
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Expandable content with enhanced styling
        with st.expander("📋 View Details", expanded=(i < 3)):
            col_left, col_right = st.columns([2, 1])

            with col_left:
                st.subheader("📄 Resume Content")
                st.text_area(
                    "Full Resume Text:",
                    value=candidate['content'][:1200] +
                    ("..." if len(candidate['content']) > 1200 else ""),
                    height=250,
                    disabled=True,
                    key=f"content_{i}")

            with col_right:
                st.subheader("📊 Score Details")
                
                # Enhanced score display
                st.markdown(f"""
                <div style="
                    background: {score_color}15;
                    padding: 1.5rem;
                    border-radius: 12px;
                    text-align: center;
                    margin: 1rem 0;
                ">
                    <div style="
                        font-size: 2.5rem;
                        font-weight: bold;
                        color: {score_color};
                        margin-bottom: 0.5rem;
                    ">
                        {score_percentage:.1f}%
                    </div>
                    <div style="color: #666; font-size: 1rem;">
                        Similarity Score
                    </div>
                    <div style="color: #888; font-size: 0.9rem; margin-top: 0.5rem;">
                        Rank #{i+1} of {len(results['top_candidates'])}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Quality indicator
                if score_percentage >= 80:
                    st.success("🏆 Excellent Match")
                elif score_percentage >= 60:
                    st.info("⭐ Good Match")
                else:
                    st.warning("📋 Fair Match")

            # Generate AI summary if enabled
            if results['generate_summaries']:
                st.markdown("---")
                with st.spinner(f"🤖 Generating AI analysis for {candidate['name']}..."):
                    try:
                        summary = results['ai_summarizer'].generate_fit_summary(
                            results['job_description'],
                            candidate['content'], 
                            candidate['similarity']
                        )

                        st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, #f8f9ff 0%, #e8f0fe 100%);
                            border-left: 4px solid #667eea;
                            padding: 2rem;
                            border-radius: 12px;
                            margin: 1rem 0;
                        ">
                            <h4 style="color: #667eea; margin: 0 0 1rem 0; font-size: 1.2rem;">
                                🤖 AI Analysis & Fit Summary
                            </h4>
                            <p style="color: #333; line-height: 1.6; margin: 0;">
                                {summary}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)

                    except Exception as e:
                        st.warning(f"⚠️ Could not generate AI summary: {str(e)}")

    # Download results option
    if st.button("📥 Download Results as CSV"):
        results_df = pd.DataFrame([{
            'Rank':
            i + 1,
            'Candidate':
            candidate['name'],
            'Similarity_Score':
            f"{candidate['similarity']:.4f}",
            'Similarity_Percentage':
            f"{candidate['similarity']:.2%}"
        } for i, candidate in enumerate(results['top_candidates'])])

        csv = results_df.to_csv(index=False)
        st.download_button(label="Download CSV",
                           data=csv,
                           file_name="candidate_recommendations.csv",
                           mime="text/csv")


def main():
    """Main application with page routing"""

    # Display the appropriate page based on session state
    if st.session_state.current_page == 'search':
        show_search_page()
    elif st.session_state.current_page == 'results':
        show_results_page()


if __name__ == "__main__":
    main()
