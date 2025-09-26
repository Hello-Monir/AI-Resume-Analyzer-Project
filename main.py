import streamlit as st
from pdfminer.high_level import extract_text
from dotenv import load_dotenv
import os
from utils.resume_ai import get_report
from utils.ats_score import calculate_similarity_bert
import re

load_dotenv()

# Session States
if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False
if "resume" not in st.session_state:
    st.session_state.resume=""
if "job_desc" not in st.session_state:
    st.session_state.job_desc=""

st.title("AI Resume Analyzer 📝")

# Functions
def extract_pdf_text(uploaded_file):
    try:
        return extract_text(uploaded_file)
    except Exception as e:
        st.error(f"Error extracting PDF: {e}")
        return "Could not extract text from PDF."

def extract_scores(text):
    pattern = r'(\d+(?:\.\d+)?)/5'
    matches = re.findall(pattern, text)
    scores = [float(match) for match in matches]
    return scores

# Workflow
if not st.session_state.form_submitted:
    with st.form("resume_form"):
        resume_file = st.file_uploader("Upload Resume PDF", type="pdf")
        st.session_state.job_desc = st.text_area(
            "Enter Job Description", placeholder="Job Description..."
        )
        submitted = st.form_submit_button("Analyze")
        if submitted:
            if resume_file and st.session_state.job_desc.strip():
                st.info("Extracting Resume Text...")
                st.session_state.resume = extract_pdf_text(resume_file)
                st.session_state.form_submitted = True
                st.rerun()
            else:
                st.warning("Please upload both Resume and Job Description.")

if st.session_state.form_submitted:
    with st.spinner("Calculating Scores..."):
        similarity_score = calculate_similarity_bert(
            st.session_state.resume, st.session_state.job_desc
        )
        report = get_report(
            st.session_state.resume, st.session_state.job_desc
        )
        report_scores = extract_scores(report)
        avg_score = sum(report_scores)/(5*len(report_scores)) if report_scores else 0

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("ATS Similarity Score")
        st.write(similarity_score)
    with col2:
        st.subheader("Average AI Report Score")
        st.write(avg_score)

    st.subheader("AI Generated Analysis Report")
    st.markdown(
        f"<div style='background-color:#000000;color:#ffffff;padding:10px;border-radius:10px'>{report}</div>",
        unsafe_allow_html=True
    )

    st.download_button(
        "Download Report",
        data=report,
        file_name="resume_analysis_report.txt",
        icon=":material/download:"
    )
