import sys
import types

try:
    import torch
    if not hasattr(torch, "classes"):
        torch.classes = types.SimpleNamespace()
except ImportError:
    pass  # if torch not yet imported

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "True"
os.environ["TOKENIZERS_PARALLELISM"] = "false"


import streamlit as st
import requests
import fitz
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# --- CONFIG ---
st.set_page_config(page_title="CareerGenie", layout="wide")
st.markdown("<style> .stButton button { background-color: #5f27cd; color: white; } </style>", unsafe_allow_html=True)

ADZUNA_APP_ID = st.secrets["ADZUNA_APP_ID"]
ADZUNA_APP_KEY = st.secrets["ADZUNA_APP_KEY"]
EMBEDDING_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

# --- FUNCTIONS ---
def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    return "\n".join([page.get_text() for page in doc])

def get_adzuna_jobs(query, location):
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
    if response.status_code != 200:
        st.error("❌ Failed to fetch jobs from Adzuna.")
        return []
    return response.json().get("results", [])

def rank_jobs(resume_text, jobs):
    resume_embedding = EMBEDDING_MODEL.encode([resume_text])[0]
    job_texts = [job["title"] + " " + job["description"] for job in jobs]
    job_embeddings = EMBEDDING_MODEL.encode(job_texts)

    job_scores = [
        (cosine_similarity([resume_embedding], [job_emb])[0][0], job)
        for job_emb, job in zip(job_embeddings, jobs)
    ]
    return sorted(job_scores, key=lambda x: x[0], reverse=True)

# --- LAYOUT ---
st.title("🔮 CareerGenie")
st.subheader("AI-Powered Job Matching with Real-Time Listings")

with st.container():
    col1, col2 = st.columns([1, 2])
    with col1:
        uploaded_file = st.file_uploader("📄 Upload your resume (PDF)", type="pdf")
    with col2:
        job_role = st.text_input("💼 Target Job Title", placeholder="e.g., Data Analyst")
        location = st.text_input("🌍 Preferred Location", placeholder="e.g., New York")

st.markdown("---")

# --- MAIN ACTION ---
if st.button("✨ Find Matching Jobs"):
    if uploaded_file:
        resume_text = extract_text_from_pdf(uploaded_file)
        st.subheader("📑 Resume Preview")
        st.code(resume_text[:700] + "...")

        with st.spinner("🔍 Finding the best jobs for you..."):
            jobs = get_adzuna_jobs(job_role, location)
            ranked_jobs = rank_jobs(resume_text, jobs)

        st.subheader("🎯 Top Job Matches")
        for score, job in ranked_jobs[:5]:
            st.markdown(f"""
                <div style="background-color: #f9f9f9; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                    <h4><a href="{job['redirect_url']}" target="_blank">{job['title']}</a></h4>
                    <p>📍 <b>{job['location']['display_name']}</b> | 💼 <b>{job['company']['display_name']}</b></p>
                    <p><b>Match Score:</b> {round(score * 100, 2)}%</p>
                    <p>{job["description"][:350]}...</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please upload your resume to begin.")
