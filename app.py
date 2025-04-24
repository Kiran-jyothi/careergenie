# app.py
import streamlit as st
import requests
import fitz
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# --- CONFIG ---
ADZUNA_APP_ID = st.secrets["ADZUNA_APP_ID"]
ADZUNA_APP_KEY = st.secrets["ADZUNA_APP_KEY"]
EMBEDDING_MODEL = SentenceTransformer("all-MiniLM-L6-v2")  # small and fast

# --- FUNCTIONS ---
def extract_text_from_pdf(uploaded_file):
    """
    Extract text from a PDF file.
    """
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    return "\n".join([page.get_text() for page in doc])

def get_adzuna_jobs(query, location):
    """
    Get job listings from Adzuna API.
    """
    url = f"https://api.adzuna.com/v1/api/jobs/us/search/1"
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "what": query,
        "where": location,
        "results_per_page": 10,
        "content-type": "application/json"
    }
    response = requests.get(url, params=params)
    return response.json().get("results", [])

def rank_jobs(resume_text, jobs):
    """
    Rank jobs based on similarity to the resume.
    """
    resume_embedding = EMBEDDING_MODEL.encode([resume_text])[0]
    job_scores = []

    for job in jobs:
        job_text = job["title"] + " " + job["description"]
        job_embedding = EMBEDDING_MODEL.encode([job_text])[0]
        score = cosine_similarity([resume_embedding], [job_embedding])[0][0]
        job_scores.append((score, job))

    ranked_jobs = sorted(job_scores, key=lambda x: x[0], reverse=True)
    return ranked_jobs

# --- STREAMLIT APP ---
st.title("CareerGenie 🔮 - AI Job Matchmaking with Real-Time Listings")

uploaded_file = st.file_uploader("📄 Upload your resume (PDF)", type="pdf")
job_role = st.text_input("💼 Target Job Title", "data analyst")
location = st.text_input("🌍 Preferred Location", "New York")

if st.button("✨ Find Matching Jobs"):
    if uploaded_file:
        resume_text = extract_text_from_pdf(uploaded_file)
        st.subheader("🔍 Your Resume (Preview)")
        st.text(resume_text[:500] + "...")

        with st.spinner("Fetching and ranking jobs..."):
            jobs = get_adzuna_jobs(job_role, location)
            ranked_jobs = rank_jobs(resume_text, jobs)

        st.subheader("🎯 Top Job Matches")
        for score, job in ranked_jobs[:5]:
            st.markdown(f"### [{job['title']}]({job['redirect_url']})")
            st.markdown(f"📍 {job['location']['display_name']} | 💼 {job['company']['display_name']}")
            st.markdown(f"**Match Score:** {round(score * 100, 2)}%")
            st.markdown(job["description"][:300] + "...")
            st.markdown("---")
    else:
        st.warning("⚠️ Please upload a resume first.")
