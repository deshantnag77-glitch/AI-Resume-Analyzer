# Vocational Training Project Report
## AI Resume Analyzer & Job Matcher

---

### 1. Introduction

In today's competitive job market, a well-structured, keyword-relevant resume significantly
improves a candidate's chances of being shortlisted. Many students, however, are unaware of
how their resume performs against automated screening or how well it matches a specific job
role. This project, **AI Resume Analyzer & Job Matcher**, addresses this gap by providing an
NLP and Machine Learning based system that analyzes a resume, estimates its ATS
compatibility, and compares it against a job description to identify skill gaps and
suggest improvements.

### 2. Problem Statement

Job seekers often submit resumes without knowing:
- Whether all standard resume sections are present and well-formed.
- Whether their resume contains the keywords and skills relevant to a target job.
- What specific, actionable changes would improve their resume.

Manually performing this analysis is time-consuming and inconsistent, and most freely
available tools either give no explanation for their scores or produce generic advice.

### 3. Objectives

1. Build a system to extract and parse resume text from PDF, DOCX, and TXT files.
2. Detect standard resume sections and identify missing ones.
3. Analyze resume text quality (length, repetition, generic phrasing, measurable results).
4. Compute an explainable, estimated ATS compatibility score.
5. Match a resume against a job description using real NLP similarity techniques.
6. Identify and prioritize skill gaps.
7. Generate specific resume improvement suggestions.
8. Implement user authentication and a personalized analysis history.

### 4. Existing System

Existing resume-checking tools generally fall into two categories: (a) manual review by
career counselors or peers, which does not scale and depends on the reviewer's expertise,
and (b) commercial online tools that return a single opaque score with little to no
explanation of the underlying methodology, sometimes encouraging users to insert keywords
they do not have genuine experience with.

### 5. Proposed System

The proposed system is a Python/Streamlit web application that performs resume analysis
locally using explainable NLP/ML techniques (TF-IDF + cosine similarity, rule-based skill
extraction, and regex-based section detection). Every score is broken down into its
component parts and explained in plain language. The system also supports user accounts
so that job seekers can track their resume's improvement over multiple analyses.

### 6. Literature / Technology Overview

- **TF-IDF (Term Frequency-Inverse Document Frequency):** A classical NLP technique for
  representing text documents as weighted vectors, giving higher weight to terms that are
  distinctive to a document relative to a corpus.
- **Cosine Similarity:** A measure of similarity between two vectors based on the cosine of
  the angle between them; widely used for comparing text documents represented as TF-IDF
  vectors.
- **Rule-based Named Entity/Skill Extraction:** Using a curated reference dataset and
  regex-based word-boundary matching to identify known entities (skills) in free text.
- **Streamlit:** A Python framework for building data-centric web applications rapidly
  without separate frontend/backend codebases.
- **SQLite:** A lightweight, file-based relational database suitable for single-application
  local deployments.

### 7. System Requirements

**Software:**
- Python 3.10+
- Streamlit, pandas, numpy, scikit-learn, pypdf, python-docx, reportlab, bcrypt

**Hardware:**
- Any standard laptop/PC capable of running Python (no GPU required)

### 8. System Architecture

The system follows a layered architecture:
- **Presentation Layer:** Streamlit multi-page interface
- **Application Layer:** Modular Python components (parsing, NLP processing, scoring,
  matching, reporting)
- **Data Layer:** SQLite database (users, profiles, settings, analysis history) and a
  local CSV skills reference dataset

### 9. Methodology

The system follows a defined pipeline: resume upload → text extraction → text cleaning →
section detection → skill/keyword extraction → job description processing → TF-IDF/
similarity analysis → skill matching → ATS score calculation → skill gap identification →
recommendation generation → dashboard display → optional PDF report.

### 10. NLP Processing

Text is cleaned (lowercased, punctuation normalized) and tokenized with a custom stopword
list. Skills are extracted using word-boundary regex matching against a structured skills
database, grouped into categories (Programming Languages, Data Science, Machine Learning,
Web Development, Databases, Cloud Technologies, DevOps, Tools, Soft Skills). Resume quality
heuristics detect repeated words, generic filler phrases, and the presence of measurable,
quantified achievements.

### 11. Machine Learning Approach

The system uses scikit-learn's `TfidfVectorizer` to convert resume and job description
text into TF-IDF vectors, then computes cosine similarity between them as a quantitative
text-relevance score. This is combined with explicit skill-set overlap (computed via set
intersection between extracted resume skills and extracted job-description skills) to
produce the final Job Match Percentage.

### 12. ATS Score Method

The Estimated ATS Compatibility Score is a weighted sum of four components, each scored
out of 25 points:
1. Structure & Section Completeness
2. Skills Relevance
3. Text Quality
4. Job Description Match

Each component's score and the reasoning behind it are displayed to the user, making the
overall score fully explainable rather than a black-box number.

### 13. Job Matching

Job Match Percentage = (0.6 × Skill Overlap %) + (0.4 × TF-IDF Cosine Similarity %).
This weighting favors explicit skill presence (which is more directly actionable for the
user) while still accounting for overall textual relevance.

### 14. Skill Gap Analysis

Skills present in the job description but absent from the resume are identified and
ranked by priority based on how frequently each skill is mentioned in the job description
text — a simple, transparent proxy for how important that skill likely is to the role.

### 15. System Implementation

The system is implemented in Python using a modular structure (see Project Structure in
README.md), separating parsing, NLP processing, scoring, matching, database access,
authentication, and reporting into independent, testable modules. SQLite is used for
persistent storage of users, profiles, settings, and analysis history, with all queries
scoped by `user_id` to ensure users can only access their own data.

### 16. User Interface

The interface is built with Streamlit and styled with a clean, white-background,
minimal-color design suitable for professional/academic presentation, with a sidebar for
navigation between Dashboard, Resume Analyzer, ATS Score, Job Matcher, Keyword Suggestions,
Skill Gap, Analysis Report, Analysis History, Profile, Settings, and About pages.

### 17. Testing

The system was tested using multiple sample resumes of varying quality (a detailed,
well-structured resume vs. a short, generic one) against a sample job description, and it
was confirmed that:
- Scores differ meaningfully between different-quality resumes.
- Scores are deterministic (the same input always produces the same output).
- Error handling correctly catches invalid files, empty resumes, and missing job
  descriptions with friendly messages instead of crashing.
- (See `TESTING.md` in the repository for the full manual test checklist.)

### 18. Results

The system successfully extracts resume content, identifies missing sections, computes an
explainable ATS score, and generates a job match percentage with matched/missing skills.
In testing, a detailed sample resume scored significantly higher (Estimated ATS
Compatibility: ~65-70/100, "Good") than a short, generic resume using cliche phrases
(~18/100, "Weak"), demonstrating that the scoring genuinely differentiates resume quality
rather than returning static or random results.

### 19. Advantages

- Fully explainable scoring — every number has a stated reason.
- Runs entirely offline/locally — no dependency on paid external APIs for core analysis.
- Modular codebase that is easy to explain, extend, and maintain.
- Personalized history lets users track resume improvement over time.
- Clear ethical guardrails: never suggests adding skills the user doesn't have.

### 20. Limitations

- The ATS score is an estimate based on this project's own methodology, not an official
  score from any commercial ATS vendor; different real systems use different algorithms.
- Skill recognition is limited to the local skills database.
- Formatting/layout analysis is limited since analysis works on extracted text.
- Extraction quality depends on the source file (scanned/image PDFs extract poorly).

### 21. Future Scope

Transformer-based semantic similarity (BERT/Sentence-BERT), automated resume section
classification via a trained classifier, personalized career recommendations, job portal
integration, multi-language support, resume version comparison, optional AI-assisted
rewriting, and cloud deployment with production-grade security.

### 22. Conclusion

AI Resume Analyzer & Job Matcher demonstrates a practical, explainable application of NLP
and Machine Learning techniques to a real-world problem faced by students and job seekers.
By combining rule-based section/skill analysis with TF-IDF-based similarity matching, the
system provides transparent, actionable feedback rather than an opaque score, while
maintaining realistic academic scope suitable for a B.Tech VT project.

### 23. References

- scikit-learn documentation: TfidfVectorizer, cosine_similarity
- Streamlit official documentation
- pypdf and python-docx library documentation
- SQLite official documentation
- bcrypt password hashing library documentation
