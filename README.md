Perfect! Here's the updated `README.md` with your live app link included:

---

# 🔮 CareerGenie

[![Streamlit App](https://img.shields.io/badge/Live%20App-CareerGenie-4b61d1?logo=streamlit&logoColor=white&labelColor=black&style=for-the-badge)](https://careergenie.streamlit.app/)

**CareerGenie** is an AI-powered job matching web app that helps job seekers find the most relevant opportunities in real time. Upload your resume, and CareerGenie uses natural language understanding and live job data to recommend roles that best align with your experience and goals.

🌐 **Try it live:** [careergenie.streamlit.app](https://careergenie.streamlit.app/)

---

## 🚀 Features

- 📄 **Resume Upload & Parsing** – Extracts skills and experience from your uploaded PDF resume.
- 🧠 **AI-Powered Matching** – Uses sentence-transformer embeddings to semantically compare your resume with job descriptions.
- 🌍 **Location-Based Search** – Enter your preferred city or region to narrow results.
- 🎓 **Experience Filter** – Choose minimum required years of experience to filter job results.
- 🔗 **Real-Time Job Listings** – Fetches live job openings using the Adzuna API.

---

## 🛠 Tech Stack

- **Frontend/UI**: [Streamlit](https://streamlit.io/)
- **NLP Model**: [`all-MiniLM-L6-v2`](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) from Sentence Transformers
- **Resume Parsing**: `PyMuPDF` (fitz)
- **Job Search API**: [Adzuna Jobs API](https://developer.adzuna.com/)
- **Similarity Calculation**: Cosine similarity via `scikit-learn`

---

## 📦 Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/careergenie.git
   cd careergenie
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate    # for Linux/Mac
   venv\Scripts\activate       # for Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Add your API credentials to `.streamlit/secrets.toml`:
   ```toml
   ADZUNA_APP_ID = "your_adzuna_app_id"
   ADZUNA_APP_KEY = "your_adzuna_app_key"
   ```

---

## 💡 How It Works

1. Upload your resume (PDF).
2. Enter your target job title and location.
3. Optionally set a minimum years of experience.
4. CareerGenie analyzes your resume and finds the best-matching live job listings based on semantic similarity.

---

## 🧪 Run Locally

```bash
streamlit run app.py
```

---

## ✨ Roadmap

- ✅ Experience filter
- ⏳ Auto-apply via API
- ⏳ Chrome extension integration
- ⏳ Job bookmarking / saving

---

## 🙌 Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Sentence Transformers](https://www.sbert.net/)
- [Adzuna Job Search API](https://developer.adzuna.com/)

---
