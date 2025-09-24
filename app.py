import streamlit as st
import os
from utils.resume_parser import extract_text_from_file
from utils.analyzer import analyze_resume, compare_with_job_description
import json
import plotly.express as px
from dotenv import load_dotenv  
load_dotenv()  


st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
        padding: 1rem;
    }
    .score-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 5px solid;
        transition: transform 0.2s ease;
    }
    .score-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
    }
    .high-score {
        border-left-color: #28a745;
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
    }
    .medium-score {
        border-left-color: #ffc107;
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
    }
    .low-score {
        border-left-color: #dc3545;
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2c3e50 0%, #3498db 100%);
    }
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    .upload-area {
        border: 2px dashed #667eea;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        background: #f8f9fa;
        margin: 1rem 0;
    }
    .result-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.8rem;
        margin: 0.2rem;
    }
    .badge-success { background: #28a745; color: white; }
    .badge-warning { background: #ffc107; color: black; }
    .badge-danger { background: #dc3545; color: white; }
</style>
""", unsafe_allow_html=True)

def main():
  
    st.markdown("""
    <div class="main-header">
        🤖 AI Resume Screening Agent
    </div>
    """, unsafe_allow_html=True)
    
   
    if 'resumes' not in st.session_state:
        st.session_state.resumes = []
    if 'job_description' not in st.session_state:
        st.session_state.job_description = ""
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    
 
    with st.sidebar:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   padding: 2rem; border-radius: 15px; color: white; margin-bottom: 2rem;'>
            <h2 style='color: white; margin-bottom: 1rem;'>🎯 Job Requirements</h2>
        </div>
        """, unsafe_allow_html=True)
        
        job_description = st.text_area(
            "**Paste the job description:**",
            height=250,
            placeholder="Enter job requirements, skills, experience needed, qualifications...",
            key="job_desc_area"
        )
        
        if st.button("💾 Save Job Description", use_container_width=True):
            if job_description.strip():
                st.session_state.job_description = job_description
                st.success("✅ Job description saved successfully!")
            else:
                st.error("Please enter a job description")
        
        st.markdown("---")
        
      
        st.markdown("""
        <div style='background: #f8f9fa; padding: 1.5rem; border-radius: 10px;'>
            <h4 style='color: #2c3e50;'>📋 How to Use</h4>
            <ol style='color: #34495e;'>
                <li>Enter job description</li>
                <li>Upload resumes (PDF/DOCX)</li>
                <li>Click 'Screen Resumes'</li>
                <li>View ranked results</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    

    col1, col2 = st.columns([2, 1])
    
    with col1:
      
        st.markdown("### 📁 Upload Resumes")
        
        with st.container():
            st.markdown('<div class="upload-area">', unsafe_allow_html=True)
            uploaded_files = st.file_uploader(
                "**Drag and drop or click to upload resumes**",
                type=['pdf', 'docx'],
                accept_multiple_files=True,
                help="Supported formats: PDF, DOCX",
                key="file_uploader"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            if uploaded_files:
                st.success(f"✅ {len(uploaded_files)} file(s) selected")
                
             
                for file in uploaded_files:
                    file_icon = "📄" if file.type == "application/pdf" else "📝"
                    st.write(f"{file_icon} {file.name}")
                
                if st.button("🚀 Screen Resumes", type="primary", use_container_width=True):
                    if not st.session_state.job_description:
                        st.error("❌ Please enter a job description first!")
                    else:
                        with st.spinner("🤖 AI is analyzing resumes... This may take a few moments."):
                            process_resumes(uploaded_files, st.session_state.job_description)
                            st.session_state.analysis_complete = True
    
    with col2:
        if st.session_state.job_description:
            st.markdown("### 📋 Current Job Description")
            with st.container():
                st.info(st.session_state.job_description[:300] + "..." 
                       if len(st.session_state.job_description) > 300 else st.session_state.job_description)
            
   
            if st.session_state.analysis_complete:
                st.markdown("### 📊 Quick Stats")
             

def process_resumes(uploaded_files, job_description):
    results = []
    
    # Progress bar with custom container
    progress_container = st.container()
    with progress_container:
        st.markdown("### 🔄 Processing Progress")
        progress_bar = st.progress(0)
        status_text = st.empty()
    
    for i, uploaded_file in enumerate(uploaded_files):
        status_text.text(f"📊 Analyzing {uploaded_file.name}... ({i+1}/{len(uploaded_files)})")
        
        try:
            # Extract text from resume
            text = extract_text_from_file(uploaded_file)
            
            if not text.strip():
                st.warning(f"⚠️ Skipped {uploaded_file.name} - no text extracted")
                continue
            
            # Analyze resume against job description
            result = compare_with_job_description(text, job_description, uploaded_file.name)
            results.append(result)
            
        except Exception as e:
            st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
        
        progress_bar.progress((i + 1) / len(uploaded_files))
    
    status_text.text("✅ Analysis complete!")
    
  
    if results:
        display_results(results)

def display_results(results):
    st.markdown("---")
    st.markdown("## 📊 Screening Results")
    
    # Sort results by score
    sorted_results = sorted(results, key=lambda x: x['overall_score'], reverse=True)
    
    # Overall ranking chart with better styling
    st.markdown("### 🏆 Candidate Ranking")
    fig = px.bar(
        x=[r['filename'] for r in sorted_results],
        y=[r['overall_score'] for r in sorted_results],
        title="Candidate Ranking by Overall Score",
        labels={'x': 'Candidates', 'y': 'Score'},
        color=[r['overall_score'] for r in sorted_results],
        color_continuous_scale='Viridis',
        height=400
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed results for each candidate
    st.markdown("### 👥 Detailed Candidate Analysis")
    for i, result in enumerate(sorted_results, 1):
        display_candidate_result(result, i)

def display_candidate_result(result, rank):
    score = result['overall_score']
    
  
    if score >= 80:
        score_class = "high-score"
        emoji = "🎯"
        badge_class = "badge-success"
        status = "Excellent Match"
    elif score >= 60:
        score_class = "medium-score"
        emoji = "⚠️"
        badge_class = "badge-warning"
        status = "Good Match"
    else:
        score_class = "low-score"
        emoji = "❌"
        badge_class = "badge-danger"
        status = "Needs Review"
    
    st.markdown(f'<div class="score-card {score_class}">', unsafe_allow_html=True)
    

    col_header1, col_header2 = st.columns([3, 1])
    with col_header1:
        st.markdown(f"### {emoji} #{rank}: {result['filename']}")
    with col_header2:
        st.markdown(f'<span class="result-badge {badge_class}">{status}</span>', unsafe_allow_html=True)
    
    # Overall score with progress bar
    st.markdown(f"**Overall Score: {score}/100**")
    st.progress(score/100)
    
    # Key metrics in a grid
    st.markdown("#### 📈 Key Metrics")
    metric_cols = st.columns(4)
    metrics = [
        ("Skills Match", result['skills_score'], "💻"),
        ("Experience", result['experience_score'], "💼"),
        ("Education", result['education_score'], "🎓"),
        ("Relevance", result['relevance_score'], "⭐")
    ]
    
    for idx, (title, value, icon) in enumerate(metrics):
        with metric_cols[idx]:
            st.markdown(f'<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f"**{icon} {title}**")
            st.markdown(f"### {value}%")
            st.progress(value/100)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Strengths and Concerns
    col_strengths, col_concerns = st.columns(2)
    
    with col_strengths:
        st.markdown("#### ✅ **Strengths**")
        for strength in result['strengths'][:4]:
            st.success(f"• {strength}")
    
    with col_concerns:
        st.markdown("#### ❌ **Areas for Improvement**")
        for concern in result['concerns'][:4]:
            st.error(f"• {concern}")
    
    # Expandable detailed analysis
    with st.expander("📋 **View Detailed Analysis**", expanded=False):
        st.markdown("#### 📝 **Summary**")
        st.info(result['summary'])
        
        if result['missing_skills']:
            st.markdown("#### 🔍 **Missing Skills**")
            for skill in result['missing_skills']:
                st.warning(f"▪️ {skill}")
        else:
            st.success("🎉 No critical skills missing!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

if __name__ == "__main__":
    # Check for API key (Google Gemini)
    api_key = os.getenv('OPENAI_API_KEY')
    
    # Debug info in sidebar
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🔧 System Info")
        if api_key:
            st.success("✅ Google Gemini API Connected")
            st.caption(f"Key: {api_key[:15]}...")
        else:
            st.error("❌ API Key Not Found")
            st.info("Set GOOGLE_API_KEY in .env file")
    
    main()