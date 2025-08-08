import streamlit as st

# Demo of enhanced UI concepts for the candidate recommendation app
st.set_page_config(
    page_title="Enhanced UI Demo - Candidate Matching",
    page_icon="🎨",
    layout="wide"
)

# Enhanced CSS styles
st.markdown("""
<style>
/* Main theme colors and gradients */
:root {
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    --card-shadow: 0 10px 25px rgba(0,0,0,0.1);
    --hover-shadow: 0 15px 35px rgba(0,0,0,0.15);
}

/* Global styling improvements */
.main > div {
    padding-top: 2rem;
}

/* Hero section with animated gradient */
.hero-section {
    background: var(--primary-gradient);
    padding: 3rem 2rem;
    border-radius: 20px;
    margin-bottom: 3rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: var(--card-shadow);
}

.hero-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
    animation: shimmer 3s infinite;
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

/* Feature cards with glassmorphism */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin: 2rem 0;
}

.feature-card {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 2rem;
    border-radius: 16px;
    text-align: center;
    transition: all 0.3s ease;
    box-shadow: var(--card-shadow);
}

.feature-card:hover {
    transform: translateY(-10px);
    box-shadow: var(--hover-shadow);
    background: rgba(255, 255, 255, 0.15);
}

.feature-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    display: block;
}

/* Enhanced input sections */
.input-section {
    background: white;
    padding: 2rem;
    border-radius: 16px;
    box-shadow: var(--card-shadow);
    margin: 1rem 0;
    border: 1px solid rgba(0,0,0,0.05);
    transition: all 0.3s ease;
}

.input-section:hover {
    box-shadow: var(--hover-shadow);
    transform: translateY(-2px);
}

.job-section {
    background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
}

.upload-section {
    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
}

/* Modern buttons */
.cta-button {
    background: var(--primary-gradient);
    color: white;
    border: none;
    padding: 1rem 3rem;
    border-radius: 50px;
    font-size: 1.2rem;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    text-decoration: none;
    display: inline-block;
    position: relative;
    overflow: hidden;
}

.cta-button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.5s;
}

.cta-button:hover::before {
    left: 100%;
}

.cta-button:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
}

/* Results page enhancements */
.results-header {
    background: var(--primary-gradient);
    color: white;
    padding: 2rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.back-button {
    background: rgba(255,255,255,0.2);
    color: white;
    border: 1px solid rgba(255,255,255,0.3);
    padding: 0.5rem 1rem;
    border-radius: 25px;
    text-decoration: none;
    transition: all 0.3s ease;
}

.back-button:hover {
    background: rgba(255,255,255,0.3);
    transform: translateX(-5px);
}

/* Candidate cards with enhanced styling */
.candidate-card {
    background: white;
    border-radius: 16px;
    box-shadow: var(--card-shadow);
    margin: 1rem 0;
    overflow: hidden;
    transition: all 0.3s ease;
    border-left: 4px solid #667eea;
}

.candidate-card:hover {
    box-shadow: var(--hover-shadow);
    transform: translateY(-2px);
}

.candidate-header {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    padding: 1.5rem;
    border-bottom: 1px solid rgba(0,0,0,0.05);
}

.match-score {
    display: inline-flex;
    align-items: center;
    background: var(--success-gradient);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 25px;
    font-weight: bold;
    box-shadow: 0 3px 10px rgba(79, 172, 254, 0.3);
}

/* Stats cards */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin: 2rem 0;
}

.stat-card {
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: var(--card-shadow);
    text-align: center;
    border-top: 3px solid #667eea;
    transition: all 0.3s ease;
}

.stat-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--hover-shadow);
}

.stat-number {
    font-size: 2rem;
    font-weight: bold;
    color: #667eea;
    margin-bottom: 0.5rem;
}

.stat-label {
    color: #6c757d;
    font-size: 0.9rem;
}

/* Progress indicators */
.progress-ring {
    width: 60px;
    height: 60px;
    position: relative;
    margin: 0 auto;
}

.progress-ring circle {
    stroke-dasharray: 188.5;
    stroke-dashoffset: 188.5;
    animation: progress 2s ease-in-out forwards;
}

@keyframes progress {
    to {
        stroke-dashoffset: calc(188.5 - (188.5 * var(--progress)) / 100);
    }
}

/* Mobile responsiveness */
@media (max-width: 768px) {
    .hero-section h1 {
        font-size: 2rem;
    }
    
    .feature-grid {
        grid-template-columns: 1fr;
    }
    
    .results-header {
        flex-direction: column;
        gap: 1rem;
    }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
    .input-section {
        background: #1e1e1e;
        color: white;
        border: 1px solid #333;
    }
    
    .candidate-card {
        background: #2d2d2d;
        color: white;
    }
    
    .stat-card {
        background: #2d2d2d;
        color: white;
    }
}
</style>
""", unsafe_allow_html=True)

# Demo content
st.markdown("""
<div class="hero-section">
    <h1>🎯 Smart Candidate Matching</h1>
    <p>AI-powered recruitment made simple, fast, and incredibly effective</p>
</div>
""", unsafe_allow_html=True)

# Feature showcase
st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <span class="feature-icon">⚡</span>
        <h3>Lightning Fast</h3>
        <p>Get results in seconds, not hours. Our AI processes hundreds of resumes instantly.</p>
    </div>
    <div class="feature-card">
        <span class="feature-icon">🎯</span>
        <h3>Precise Matching</h3>
        <p>Advanced algorithms ensure the most relevant candidates rise to the top.</p>
    </div>
    <div class="feature-card">
        <span class="feature-icon">🧠</span>
        <h3>Smart Insights</h3>
        <p>Get AI-powered explanations for why each candidate is a great fit.</p>
    </div>
    <div class="feature-card">
        <span class="feature-icon">📊</span>
        <h3>Rich Analytics</h3>
        <p>Detailed metrics and visualizations to make informed hiring decisions.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Input sections demo
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="input-section job-section">', unsafe_allow_html=True)
    st.header("📋 Job Description")
    st.text_area("Enter job requirements:", height=200, placeholder="Describe the perfect candidate...")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="input-section upload-section">', unsafe_allow_html=True)
    st.header("📄 Upload Resumes")
    st.file_uploader("Choose files", accept_multiple_files=True, type=['pdf', 'txt', 'docx'])
    st.markdown('</div>', unsafe_allow_html=True)

# Enhanced CTA button
st.markdown("""
<div style="text-align: center; margin: 3rem 0;">
    <button class="cta-button">🚀 Analyze Candidates</button>
</div>
""", unsafe_allow_html=True)

# Results page demo
st.markdown("---")
st.header("Results Page Preview")

st.markdown("""
<div class="results-header">
    <div>
        <h2>🏆 Top Candidates Found</h2>
        <p>Analysis completed for Software Developer position</p>
    </div>
    <button class="back-button">← Back to Search</button>
</div>
""", unsafe_allow_html=True)

# Stats grid
st.markdown("""
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-number">24</div>
        <div class="stat-label">Candidates Analyzed</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">87%</div>
        <div class="stat-label">Average Match Score</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">3.2s</div>
        <div class="stat-label">Processing Time</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">8</div>
        <div class="stat-label">Excellent Matches</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sample candidate cards
for i in range(3):
    st.markdown(f"""
    <div class="candidate-card">
        <div class="candidate-header">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3 style="margin: 0;">#{i+1} - John Smith</h3>
                    <p style="margin: 0.5rem 0; color: #666;">Senior Software Developer</p>
                </div>
                <div class="match-score">
                    {95-i*5}% Match
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.header("UI Enhancement Summary")

st.info("""
**Key Visual Improvements Demonstrated:**
- Modern gradient backgrounds and glassmorphism effects
- Enhanced typography with better hierarchy
- Animated hover effects and transitions  
- Professional color scheme with consistent branding
- Mobile-responsive grid layouts
- Enhanced buttons with shimmer effects
- Clean card-based layouts with subtle shadows
- Progress indicators and data visualizations
""")

st.success("""
**Next Steps for Implementation:**
1. Apply these styles to your main app.py file
2. Add interactive animations and micro-interactions
3. Implement responsive design for mobile devices
4. Add data visualization components (charts, progress bars)
5. Create a cohesive design system with consistent spacing and colors
""")

st.markdown("""
**Additional Features to Consider:**
- Dark/light mode toggle
- Custom branding options
- Advanced filtering and sorting
- Export functionality with branded PDFs
- User dashboards and analytics
- Team collaboration features
""")