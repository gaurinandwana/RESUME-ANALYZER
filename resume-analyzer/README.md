# 🎯 AI Resume Analyzer

An intelligent, full-stack local web application that evaluates a candidate's PDF resume against any target Job Description (JD). Built with Python, Streamlit, Scikit-Learn, and NLP techniques, it provides a transparent **Resume Match Score (0–100%)**, skill gap identification, keyword metrics, structure audits, actionable feedback, and downloadable reports — **100% locally without requiring paid API keys**.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red.svg)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-TF--IDF-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 🌟 Key Features

1. **📄 PDF Resume Parsing & Text Extraction**
   - Automatically extracts clean text from text-selectable PDF resumes using `PyPDF2`.
   - Computes document statistics: page count, word count, character count.
   - Robust error handling for corrupt, password-protected, or unreadable scanned PDFs.

2. **🛠️ Comprehensive Skill Extraction & Categorization**
   - Built-in skills database covering 65+ technical skills, frameworks, databases, cloud tools, AI/ML libraries, and soft skills.
   - Regex-based word boundary matcher handles complex tokens (e.g. `C++`, `C#`, `Node.js`, `REST API`).
   - Normalizes variations (`React.js` -> `React`, `sklearn` -> `Scikit-learn`, `amazon web services` -> `AWS`).

3. **📊 Transparent Resume Match Scoring (0–100%)**
   - **No fake or randomized AI scores!** Calculated using a deterministic, transparent weighted formula:
     - **40% Technical Skill Match Ratio**: Matched vs required JD skills.
     - **20% Keyword Relevance**: TF-IDF domain terminology extraction.
     - **15% Experience Alignment**: Experience sections & years of experience detected.
     - **15% Education Alignment**: Degree requirements & major verification.
     - **10% Textual Similarity**: Cosine similarity between resume TF-IDF vector & JD text vector.

4. **🔍 Skill Gap & Keyword Analysis**
   - Displays **Skills You Have** (green badges) and **Skills You May Be Missing** (red badges sorted by frequency in JD).
   - Category-wise Matplotlib bar chart visualizer.
   - Matched vs Missing domain keyword lists.

5. **📑 Resume Structure & Quality Audit**
   - Automated detection of essential sections: Contact Information, Summary, Education, Experience, Projects, Skills, Certifications, Achievements, Extracurriculars.
   - Quality checks for word count length, quantifiable achievements (metrics/percentages), and active action verbs.
   - Practical bullet rewrite examples (e.g. converting "Worked on web app" to "Developed web application used by 500+ daily users").

6. **💡 Actionable Improvement Recommendations**
   - Tailored advice on missing skills and sections without encouraging false skill claims.

7. **📥 Downloadable Analysis Report**
   - Dynamic report generator exports complete results as a formatted `.txt` file with one click.

8. **🔒 100% Local & Private**
   - Operates in-memory on your machine. Resumes are never stored permanently or uploaded to third-party cloud services.

---

## 🚀 Tech Stack

- **Frontend & Framework**: [Streamlit](https://streamlit.io/)
- **Programming Language**: Python 3.9+
- **Data Processing**: Pandas, NumPy
- **Natural Language Processing & ML**: Scikit-Learn (`TfidfVectorizer`, `cosine_similarity`)
- **PDF Text Extraction**: PyPDF2
- **Data Visualization**: Matplotlib

---

## 📂 Project Architecture

```
resume-analyzer/
│
├── app.py                 # Streamlit UI layout, state management & dashboard
├── resume_parser.py       # PDF text extraction, section audit & quality rules
├── skills.py              # Skill database, normalization & regex extraction
├── analyzer.py            # Transparent scoring algorithm, TF-IDF & keyword matcher
├── report_generator.py    # Downloadable plain text/markdown report generator
├── vercel.json            # Vercel deployment configuration
├── requirements.txt       # Dependencies
├── README.md              # Project documentation
└── .gitignore             # Git ignore configuration
```

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.9 or higher installed on your system.

### Step 1: Clone or Download the Project
```bash
git clone https://github.com/gaurinandwana/RESUME-ANALYZER.git
cd RESUME-ANALYZER
```

### Step 2: Create a Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 💻 How to Run Locally

Launch the Streamlit web application with:

```bash
streamlit run app.py
```

The application will open automatically in your browser at `http://localhost:8501`.

---

## 🌐 Deployment Instructions

### Deploying on Vercel
This project includes a pre-configured `vercel.json` file for Vercel Python Serverless execution:

1. Push your repository changes to GitHub.
2. Log in to your [Vercel Dashboard](https://vercel.com/) and click **"Add New Project"**.
3. Import your GitHub repository (`RESUME-ANALYZER`).
4. Vercel automatically detects `vercel.json` and installs Python dependencies from `requirements.txt`.
5. Click **"Deploy"**.

---

### Deploying on Streamlit Community Cloud (Recommended)
Streamlit Cloud offers free 1-click hosting natively tailored for Streamlit apps:

1. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with GitHub.
2. Click **"New App"**.
3. Select repository: `gaurinandwana/RESUME-ANALYZER`, Branch: `main`, Main file path: `app.py`.
4. Click **"Deploy!"**.

---

## 📈 Scoring Methodology

The Resume Match Score is computed deterministically using the following weighted model:

$$\text{Score} = (W_{\text{skills}} \times S_{\text{skills}}) + (W_{\text{keywords}} \times S_{\text{keywords}}) + (W_{\text{exp}} \times S_{\text{exp}}) + (W_{\text{edu}} \times S_{\text{edu}}) + (W_{\text{similarity}} \times S_{\text{similarity}})$$

| Component | Default Weight | Description |
| :--- | :--- | :--- |
| **Technical Skill Match** | **40%** | Ratio of matched technical skills to total skills present in JD |
| **Keyword Relevance** | **20%** | Ratio of matched domain terms extracted via TF-IDF |
| **Experience Alignment** | **15%** | Verification of work experience section and years of experience |
| **Education Alignment** | **15%** | Detection of degree and academic credentials |
| **Textual Similarity** | **10%** | TF-IDF Cosine Similarity between entire resume text and JD |

---

## 🛡️ Privacy Guarantee

Your data privacy is guaranteed. All PDF extraction, text processing, and scoring logic occur locally within your Python session in memory. No resume content is stored on disk or sent over any network interface.
