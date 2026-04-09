import streamlit as st
import pandas as pd
from processor import parse_resume, clean_text
from matcher import match_resume
import io

# Page Configuration
st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="📄",
    layout="wide"
)

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .skill-tag {
        display: inline-block;
        padding: 2px 10px;
        margin: 2px;
        border-radius: 15px;
        background-color: #e9ecef;
        font-size: 0.8em;
    }
    .match-tag {
        background-color: #d4edda;
        color: #155724;
    }
    .missing-tag {
        background-color: #f8d7da;
        color: #721c24;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 AI Resume Screening & Ranking System")
st.markdown("---")

# Layout: Sidebar for Job Description
with st.sidebar:
    st.header("Job Role Setup")
    job_description = st.text_area(
        "Paste Job Description here:",
        height=300,
        placeholder="We are looking for a Python Developer with experience in Django, React, and SQL..."
    )
    st.info("The system will extract skills from this JD to compare against resumes.")

# Main Area: Resume Upload
st.header("Upload Resumes")
uploaded_files = st.file_uploader(
    "Choose Resume Files (PDF, DOCX, TXT)",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

if uploaded_files and job_description:
    st.markdown("### Screening Results")
    
    results = []
    
    # Process each resume
    with st.spinner("Analyzing resumes..."):
        clean_jd = clean_text(job_description)
        
        for uploaded_file in uploaded_files:
            file_bytes = uploaded_file.read()
            raw_text = parse_resume(file_bytes, uploaded_file.name)
            
            if "Error" in raw_text or raw_text == "Unsupported file format":
                st.error(f"Could not parse {uploaded_file.name}: {raw_text}")
                continue
                
            clean_resume = clean_text(raw_text)
            match_data = match_resume(clean_resume, clean_jd)
            
            results.append({
                "Candidate Name": uploaded_file.name,
                "Match Score (%)": match_data["score"],
                "Skills Found": match_data["resume_skills"],
                "Matched Skills": match_data["matched_skills"],
                "Missing Skills": match_data["missing_skills"]
            })

    if results:
        # Convert to DataFrame and Rank
        df = pd.DataFrame(results)
        df = df.sort_values(by="Match Score (%)", ascending=False)
        
        # Display Ranking Table
        st.dataframe(
            df[["Candidate Name", "Match Score (%)"]],
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown("---")
        st.header("Detailed Analysis")
        
        # Selection for detailed view
        selected_candidate = st.selectbox("Select a candidate to view details:", df["Candidate Name"])
        
        if selected_candidate:
            cand_data = df[df["Candidate Name"] == selected_candidate].iloc[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Overall Match Score", f"{cand_data['Match Score (%)']}%")
                
                st.subheader("Skills Found in Resume")
                skills_html = "".join([f'<span class="skill-tag">{s}</span>' for s in cand_data["Skills Found"]])
                st.markdown(skills_html, unsafe_allow_html=True)

            with col2:
                st.subheader("✅ Matched Skills")
                matched_html = "".join([f'<span class="skill-tag match-tag">{s}</span>' for s in cand_data["Matched Skills"]])
                st.markdown(matched_html if matched_html else "No matches found.", unsafe_allow_html=True)
                
                st.subheader("❌ Missing Skills (Gaps)")
                missing_html = "".join([f'<span class="skill-tag missing-tag">{s}</span>' for s in cand_data["Missing Skills"]])
                st.markdown(missing_html if missing_html else "No gaps identified!", unsafe_allow_html=True)

elif not job_description:
    st.warning("Please provide a Job Description in the sidebar.")
elif not uploaded_files:
    st.info("Awaiting resume uploads...")

st.markdown("---")
st.caption("Built with ❤️ using Python, spaCy, and Streamlit.")
