# 🎯 AI Resume Screening System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3.3-000000?style=for-the-badge&logo=flask&logoColor=white)
![spaCy](https://img.shields.io/badge/spaCy-3.7.2-09A3D5?style=for-the-badge&logo=spacy&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3.0-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

An intelligent NLP-powered web application that automatically screens resumes against job descriptions and provides a detailed match score with HR recommendations.

</div>

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [How It Works](#-how-it-works)
- [Scoring System](#-scoring-system)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [Usage](#-usage)
- [Screenshots](#-screenshots)
- [Team](#-team)

---

## 🧠 Overview

The **AI Resume Screening System** solves a real-world HR problem — manually reading hundreds of resumes is slow and inconsistent. This system uses **Artificial Intelligence and Natural Language Processing (NLP)** to:

- Read and understand resume PDFs
- Compare them against a job description
- Generate an intelligent match score out of 100%
- Provide detailed feedback and HR recommendations

> Instead of simple keyword matching, our system understands the **meaning** behind the text using advanced NLP techniques like semantic similarity, TF-IDF, and named entity recognition.

---

## ✅ Features

| Feature | Description |
|---|---|
| 📄 PDF Resume Upload | Upload any PDF resume for analysis |
| 💼 Job Description Input | Paste any job description to compare against |
| 🧠 AI Match Scoring | Get a match score out of 100% using 4 NLP methods |
| 🔧 Skills Detection | Automatically detects 60+ technical & soft skills |
| 🏷️ Candidate Classification | Outstanding / Good / Potential / Low / Not Suitable |
| 💡 Detailed Feedback | Tone analysis, key strengths, education & experience insights |
| 🔑 Key Phrases | Extracts meaningful phrases from the resume |
| 📊 Screening History | All past results stored and viewable anytime |
| ✉️ HR Recommendation | Clear interview recommendation for each candidate |

---

## ⚙️ How It Works

```
User uploads PDF Resume + pastes Job Description
              ↓
     app.py receives the request
              ↓
  resume_processor.py extracts PDF text
              ↓
     NLP cleaning (lemmatization, stopword removal)
              ↓
   ┌──────────────────────────────────────┐
   │  4 Scoring Methods Applied:          │
   │  • Semantic Similarity (spaCy)       │
   │  • TF-IDF Match (scikit-learn)       │
   │  • Keyword Matching                  │
   │  • Entity Matching (skills/edu)      │
   └──────────────────────────────────────┘
              ↓
     Weighted Final Score Calculated
              ↓
   Skills, Phrases, Sentiment Extracted
              ↓
   Result saved to SQLite Database
              ↓
     Results page displayed to user
```

---

## 📊 Scoring System

The final score is a weighted combination of **4 NLP techniques**:

| Method | Weight | Description |
|---|---|---|
| 🔵 Semantic Similarity | **40%** | Uses spaCy word vectors to understand the *meaning* of text — not just matching words |
| 🟢 TF-IDF Match | **30%** | Ranks words by importance and checks how many high-value job description terms appear in the resume |
| 🟡 Keyword Matching | **20%** | Direct word-to-word overlap between resume and job description |
| 🔴 Entity Matching | **10%** | Checks if specific skills and education keywords from the job description exist in the resume |

### 🏷️ Classification Table

| Score Range | Classification | Recommendation |
|---|---|---|
| ≥ 80% | 🟢 Outstanding Match | Highly recommended for interview |
| 65% – 79% | 🔵 Good Match | Recommended for interview |
| 50% – 64% | 🟡 Potential Match | Consider for further review |
| 35% – 49% | 🟠 Low Match | Keep as backup candidate |
| < 35% | 🔴 Not Suitable | Does not meet requirements |

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Backend | Python 3.8+, Flask 2.3.3 |
| NLP & AI | spaCy 3.7.2, NLTK 3.8.1, TextBlob 0.17.1 |
| Machine Learning | scikit-learn 1.3.0, NumPy 1.24.3 |
| PDF Processing | PyPDF2 3.0.1 |
| Database | SQLite (via Python sqlite3) |
| Frontend | HTML5, CSS3, Jinja2 Templates |

---

## 📁 Project Structure

```
ai-resume-screening/
│
├── app.py                  # Main Flask web server & routes
├── resume_processor.py     # Core AI & NLP logic
├── database.py             # SQLite database management
├── requirements.txt        # Python dependencies
│
├── templates/
│   ├── base.html           # Base layout with navbar
│   ├── index.html          # Home page (upload form)
│   ├── results.html        # Analysis results page
│   └── history.html        # Screening history page
│
├── static/
│   └── css/
│       └── style.css       # Stylesheet
│    └── js/
│       └── main.js  
└── uploads/                # Temporary PDF storage (auto-created)
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1 — Clone the Repository
```bash
git clone https://github.com/moheezkiani01/ai-resume-screening.git
cd ai-resume-screening
```

### Step 2 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Download spaCy Language Model
```bash
python -m spacy download en_core_web_md
```

### Step 4 — Download NLTK Data
```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('punkt')"
```

### Step 5 — Run the Application
```bash
python app.py
```

### Step 6 — Open in Browser
```
http://localhost:5000
```

---

## 📖 Usage

1. Go to the **Home** page
2. Click **Upload Resume** and select a PDF file
3. Paste the **Job Description** into the text box
4. Click **Analyze Resume**
5. View your detailed AI analysis results including:
   - Overall match score
   - Skills detected
   - NLP insights & feedback
   - HR recommendation
6. Visit **History** to see all past screenings

---

**Instructor:** Sir Philemon Philip

---

## 📄 License

This project is for educational purposes under Superior University, Lahore.

---
</div>
