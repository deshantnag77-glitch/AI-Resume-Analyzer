# AI Resume Analyzer & Job Matcher

AI-powered Resume Analysis, ATS Score Checking and Job Skill Matching System.

## Overview

AI Resume Analyzer & Job Matcher is a Python-based web application built with Streamlit that helps students and job seekers analyze their resumes using NLP and Machine Learning techniques.

Users can upload a resume in PDF, DOCX, or TXT format and optionally provide a job description. The system analyzes the resume and provides an estimated ATS compatibility score, job match percentage, skill gap analysis, keyword suggestions, and practical resume improvement recommendations.

This project was developed as a B.Tech IT Vocational Training (VT) project.

## Problem Statement

Many students and job seekers do not know:

- Whether their resume is ATS-friendly.
- How well their resume matches a specific job description.
- Which skills or keywords are missing.
- How to improve their resume effectively.
- Which areas of their resume need improvement.

Manually comparing a resume with a job description can be time-consuming and error-prone.

## Objectives

- Automatically extract and analyze resume content.
- Detect standard resume sections.
- Generate an explainable estimated ATS compatibility score.
- Compare resumes with job descriptions using NLP techniques.
- Identify matched and missing skills and keywords.
- Identify important skill gaps.
- Provide actionable resume improvement suggestions.
- Allow users to save and revisit their analysis history.

## Features

- Resume upload support for PDF, DOCX, and TXT.
- Resume text extraction.
- Resume section detection.
- Resume quality analysis.
- Estimated ATS Compatibility Score.
- ATS score component breakdown.
- Job Description matching.
- TF-IDF and cosine similarity analysis.
- Skill matching.
- Keyword suggestions.
- Skill gap identification.
- High/Medium/Low priority skill gaps.
- Downloadable PDF analysis report.
- User registration and login.
- Password hashing.
- Personalized user dashboard.
- Analysis history.
- User profile and settings.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application framework |
| NLP | Resume and job description analysis |
| Scikit-learn | TF-IDF and cosine similarity |
| Pandas | Data processing |
| NumPy | Numerical operations |
| PyPDF | PDF text extraction |
| python-docx | DOCX text extraction |
| SQLite | Database |
| bcrypt | Password hashing |
| ReportLab | PDF report generation |
| Plotly | Data visualization |

## System Architecture

```text
User
 |
 v
Login / Register
 |
 v
User Dashboard
 |
 v
Resume Upload
 |
 v
Text Extraction
 |
 v
Text Cleaning
 |
 +----------------------+
 |                      |
 v                      v
Section Detection    Skill Extraction
 |                      |
 +----------+-----------+
            |
            v
    Job Description
       Processing
            |
            v
   TF-IDF + Cosine
      Similarity
            |
            v
     Skill Matching
            |
            v
    ATS Score Analysis
            |
            v
     Skill Gap Analysis
            |
            v
     Recommendations
            |
            v
     Save Analysis
            |
            v
     PDF Report