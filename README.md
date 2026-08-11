# AI Resume Analyzer & Job Matcher

AI-powered Resume Analysis, ATS Score Checking and Job Skill Matching System

## Overview

AI Resume Analyzer & Job Matcher is a Python-based web application built with Streamlit
that helps students and job seekers analyze their resumes using NLP and Machine Learning
techniques. Users can upload a resume (PDF/DOCX/TXT), optionally paste a job description,
and receive an estimated ATS compatibility score, a job match percentage, skill gap
analysis, keyword suggestions, and practical resume improvement recommendations.

This project was built as a B.Tech IT Vocational Training (VT) project.

## Problem Statement

Many students and job seekers do not know:
- Whether their resume is structured in a way that automated screening systems can parse.
- How well their resume actually matches a specific job description.
- Which specific skills or keywords they are missing for a target role.
- How to improve their resume beyond vague advice like "make it better."

Manually comparing a resume against a job description and figuring out what to add is
time-consuming and error-prone.

## Objectives

- Extract and analyze resume content automatically.
- Detect standard resume sections and flag missing ones.
- Generate an explainable, estimated ATS compatibility score.
- Compare a resume against a job description using real NLP similarity techniques.
- Identify matched and missing skills/keywords.
- Prioritize skill gaps based on relevance to the job description.
- Provide specific, actionable resume improvement suggestions.
- Allow registered users to save and revisit their analysis history.

## Features

- Resume upload (PDF, DOCX, TXT) with text extraction
- Section detection (contact info, education, skills, projects, experience, etc.)
- Resume quality analysis (length, repetition, generic phrases, measurable achievements)
- Estimated ATS Compatibility Score with component-level breakdown
- Job Description matching (TF-IDF cosine similarity + skill overlap)
- Keyword suggestions grouped by category
- Skill gap analysis with High/Medium/Low learning priority
- Downloadable PDF analysis report
- User authentication (registration/login) with hashed passwords
- Personalized dashboard and analysis history
- Editable user profile and analysis settings

## Technology Stack

- **Language:** Python 3.10+
- **Web Framework:** Streamlit
- **NLP / ML:** scikit-learn (TF-IDF, cosine similarity), regex-based rule matching
- **Data Handling:** pandas, numpy
- **File Parsing:** pypdf, python-docx
- **Database:** SQLite
- **Authentication:** bcrypt (password hashing)
- **Reporting:** ReportLab (PDF generation)
- **Visualization:** Streamlit native components, Plotly (optional)

## System Architecture

```
Login / Register
        |
User Dashboard
        |
Resume Upload -> Text Extraction -> Text Cleaning
        |
Section Detection -> Skill & Keyword Extraction
        |
Job Description Processing (optional)
        |
TF-IDF / Cosine Similarity Analysis
        |
Skill Matching -> ATS Compatibility Calculation
        |
Skill Gap Identification -> Recommendations
        |
Save Analysis -> Analysis History -> PDF Report
```

## NLP/ML Methodology

1. **Text Extraction:** `pypdf` for PDF, `python-docx` for DOCX, direct decoding for TXT.
2. **Text Cleaning:** Lowercasing, punctuation normalization, stopword removal.
3. **Section Detection:** Regex-based heading/keyword matching against a curated list of
   standard resume section patterns.
4. **Skill Extraction:** Word-boundary regex matching against a local skills database
   (`data/skills.csv`) covering programming languages, data science, ML, web, databases,
   cloud, DevOps and soft skills.
5. **Similarity Analysis:** TF-IDF vectorization of resume and job description text,
   followed by cosine similarity — a standard, explainable NLP technique (no black-box
   deep learning models required, so the project runs fully offline).

## ATS Scoring Methodology

The Estimated ATS Compatibility Score (0–100) is composed of four equally-weighted
components (25 points each):

| Component | What it measures |
|---|---|
| Structure & Section Completeness | Fraction of standard resume sections detected |
| Skills Relevance | Breadth of recognized skills found in the resume |
| Text Quality | Length, repetition, generic phrasing, measurable achievements |
| Job Description Match | TF-IDF + skill-overlap match against the pasted JD (or a conservative skill-only estimate if no JD is given) |

This is **not** a claim of replicating any specific commercial ATS vendor's proprietary
algorithm — it is a transparent, project-specific heuristic model designed to be explainable
to a non-technical reader.

## Job Matching Methodology

```
Job Match % = (0.6 × Skill Overlap %) + (0.4 × TF-IDF Cosine Similarity %)
```

- **Skill Overlap %** = (skills in both resume and JD) / (total skills required by JD)
- **TF-IDF Cosine Similarity** = standard vector-space text similarity between the two documents

## Skill Gap Analysis

Skills required by the job description but absent from the resume are flagged as gaps and
assigned a priority:

- **High Priority** — mentioned 3+ times in the job description
- **Medium Priority** — mentioned 2 times
- **Low Priority** — mentioned once

## Project Structure

```
AI_Resume_Analyzer/
│
├── app.py                     # Main Streamlit application
├── database.py                 # SQLite database layer
├── auth.py                     # Authentication logic (register/login/hashing)
├── requirements.txt
├── README.md
├── LICENSE
├── ORIGINALITY.md
├── IP_DOCUMENTATION.md
├── .gitignore
│
├── modules/
│   ├── resume_parser.py        # PDF/DOCX/TXT text extraction
│   ├── text_processor.py       # Cleaning, tokenization, quality heuristics
│   ├── section_detector.py     # Resume section detection
│   ├── skill_extractor.py      # Skill/keyword extraction against skills.csv
│   ├── ats_scorer.py           # Estimated ATS Compatibility scoring
│   ├── job_matcher.py          # TF-IDF + skill matching
│   ├── keyword_analyzer.py     # Missing keyword grouping
│   ├── skill_gap.py            # Skill gap + priority logic
│   ├── suggestions.py          # Resume improvement suggestions
│   └── report_generator.py     # PDF report generation
│
├── data/
│   └── skills.csv              # Local skills/technology database
│
├── database/
│   └── resume_analyzer.db      # SQLite database (created at runtime, not committed)
│
└── assets/
    └── screenshots/
```

## Installation

```bash
git clone <repository-url>
cd AI_Resume_Analyzer
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## How to Run

```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`. On first run, it automatically
creates the SQLite database and required tables.

## Screenshots

_Add screenshots of the Dashboard, Resume Analyzer, ATS Score, and Job Matcher pages here
after running the app (`assets/screenshots/`)._

## Future Scope

- Transformer-based semantic similarity (e.g., BERT/Sentence-BERT) for deeper matching
- Automated resume section classification using a trained ML classifier
- Personalized career/learning path recommendations
- Job portal API integration for live job description fetching
- Multi-language resume analysis
- Resume version comparison over time
- AI-assisted resume rewriting suggestions (as an optional, clearly-labeled feature)
- Cloud deployment with proper production-grade security hardening
- Analytics dashboard aggregating trends across a user's analysis history

## Limitations

- The ATS score is an **estimated compatibility score** based on this project's own
  methodology — it does not represent an official score from any real ATS vendor.
- Different commercial ATS systems use different, proprietary algorithms.
- Skill extraction is limited to the local skills database and may not recognize every
  possible technology, tool, or emerging skill.
- Formatting/layout analysis (fonts, images, columns) is limited since analysis works on
  extracted text, not visual layout.
- Results depend on the quality of text extracted from the uploaded file (e.g., scanned/
  image-based PDFs may extract poorly).
- The system deliberately avoids recommending that users add skills they do not genuinely
  have or have not used.
- Basic application-level security practices have been implemented (password hashing,
  session-based access control, user-scoped data access). Production deployment would
  require additional security hardening (HTTPS enforcement, rate limiting, CSRF protection,
  etc.).

## Author / Developer

Developed as a B.Tech IT Vocational Training project.
_Add your name, roll number, college and guide's name here._
