import streamlit as st
from pdfminer.high_level import extract_text
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from io import BytesIO

from ats_score import keyword_overlap_score
from resume_ai import suggest_improvements, try_groq_rewrite
from azure_llm import try_azure_rewrite
from storage import upload_to_blob
from utils import clean_text

st.set_page_config(page_title="AI Resume Analyzer (Azure-ready)", page_icon="🧭", layout="wide")

@st.cache_resource
def get_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

def read_pdf_text(pdf_file) -> str:
    return extract_text(pdf_file)

def embed(texts, model):
    embeddings = model.encode(texts, normalize_embeddings=True)
    if isinstance(embeddings, list):
        embeddings = np.array(embeddings)
    return embeddings

def compute_similarity(a: str, b: str, model) -> float:
    embs = embed([a, b], model)
    sim = float(cosine_similarity(embs[0:1], embs[1:2])[0][0])
    return round(sim, 4)

st.title("AI Resume Analyzer")
st.caption("ATS coverage, semantic fit, and optional Azure/Groq rewrite suggestions.")

col1, col2 = st.columns(2)
with col1:
    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    resume_text = ""
    uploaded_url = None
    if resume_file:
        # Keep a copy of bytes for Azure Blob if enabled
        resume_bytes = resume_file.getvalue()
        resume_text = clean_text(read_pdf_text(BytesIO(resume_bytes)))
        if st.checkbox("Upload a copy to Azure Blob (optional)"):
            url = upload_to_blob(resume_bytes, blob_name=resume_file.name)
            uploaded_url = url
            if isinstance(url, str) and url.startswith("http"):
                st.success(f"Uploaded to: {url}")
            elif url:
                st.warning(str(url))

with col2:
    jd_text = st.text_area("Paste Job Description", height=260)

analyze = st.button("Analyze")

if analyze:
    if not resume_file or not jd_text.strip():
        st.error("Provide both a resume PDF and a job description.")
        st.stop()

    model = get_model()
    sim = compute_similarity(resume_text, jd_text, model)

    ats = keyword_overlap_score(resume_text, jd_text)
    tips = suggest_improvements(sim, ats["score"])

    st.subheader("Fit Summary")
    st.metric("Semantic Similarity", f"{sim:.2f}", help="0–1. Values closer to 1 indicate stronger semantic alignment.")
    st.metric("ATS Keyword Coverage", f"{ats['score']}%", help="Percentage of JD keywords found in resume.")
    if uploaded_url:
        st.write(f"Azure Blob copy: {uploaded_url}")

    with st.expander("Matched Keywords"):
        st.write(", ".join(ats["matched_keywords"]) or "None")

    with st.expander("Missing Keywords"):
        st.write(", ".join(ats["missing_keywords"]) or "None")

    st.subheader("Suggestions")
    st.markdown(tips["suggestions"])

    st.subheader("LLM Rewrite (optional)")
    tab1, tab2 = st.tabs(["Azure OpenAI", "Groq"])

    with tab1:
        rewrite = try_azure_rewrite(resume_text, jd_text)
        if rewrite is None:
            st.info("Set AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, and AZURE_OPENAI_DEPLOYMENT in .env to enable Azure OpenAI.")
        else:
            st.write(rewrite)

    with tab2:
        rewrite_g = try_groq_rewrite(resume_text, jd_text)
        if rewrite_g is None:
            st.info("Set GROQ_API_KEY in .env to enable Groq-powered rewrites.")
        else:
            st.write(rewrite_g)
else:
    st.info("Upload a sample resume from sample_data/ and paste the sample JD to try. Azure and Groq are optional.")

st.markdown("---")
st.caption("Local use only. Do not upload confidential data without permission.")
