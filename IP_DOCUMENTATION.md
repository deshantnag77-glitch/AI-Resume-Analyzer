# IP Documentation

## 1. Invention/Project Title

AI Resume Analyzer & Job Matcher

## 2. Technical Problem

Students and early-career job seekers often lack the tools or expertise to evaluate
whether their resume is structurally sound, whether it is likely to be parsed correctly
by automated screening tools, and how closely it matches the specific requirements of a
target job posting. Existing approaches to this problem tend to be either purely manual
(a person reading the resume and JD side by side) or opaque commercial tools that return a
single score with no explanation of how it was derived, making it difficult for the user
to know what to actually improve.

## 3. Existing Approach

- **Manual comparison:** A job seeker reads the job description and their resume and
  tries to spot gaps themselves. This is time-consuming, inconsistent, and easy to miss
  details in.
- **Basic keyword checkers:** Some existing tools simply count keyword occurrences without
  explaining structure, section completeness, or providing a breakdown of how a score was
  computed.
- **Commercial ATS-simulation tools:** Often present a single opaque score without
  disclosing the underlying methodology, and may encourage keyword-stuffing without
  regard for whether the user genuinely has the relevant skill or experience.

## 4. Proposed System

This project proposes an integrated, explainable pipeline that combines resume structural
analysis, rule-based skill/keyword extraction, and NLP-based text similarity (TF-IDF +
cosine similarity) into a single, transparent scoring and recommendation system, with a
user-scoped history of past analyses. Every score component is broken down and explained
to the user rather than presented as an opaque number.

## 5. System Architecture

- **Presentation layer:** Streamlit-based multi-page web interface.
- **Application logic layer:** Modular Python components for parsing, text processing,
  section detection, skill extraction, scoring, matching, keyword analysis, skill gap
  analysis, and suggestion generation (`modules/`).
- **Data layer:** SQLite database storing users, profiles, settings, and analysis history;
  a local CSV-based skills reference dataset (`data/skills.csv`).
- **Authentication layer:** Session-based authentication with bcrypt password hashing.
- **Reporting layer:** PDF report generation via ReportLab.

## 6. Technical Workflow

```
Resume Upload
   -> Text Extraction (PDF/DOCX/TXT parsing)
   -> NLP Preprocessing (cleaning, tokenization, stopword removal)
   -> Section Detection (regex-based heading/content matching)
   -> Skill Extraction (word-boundary matching against skills database)
   -> Job Description Processing (same cleaning/extraction pipeline applied to JD text)
   -> TF-IDF / Similarity Analysis (vectorization + cosine similarity)
   -> Skill Matching (set comparison between resume skills and JD skills)
   -> ATS Compatibility Calculation (weighted four-component score)
   -> Skill Gap Identification (missing skills ranked by JD mention frequency)
   -> Recommendations (derived directly from detected issues, not generic text)
```

## 7. Potentially Distinctive Combination

The system combines the following elements into a single explainable pipeline:

- Resume structural/section analysis
- Rule-based keyword and skill-category analysis
- TF-IDF-based NLP similarity between resume and job description
- Explicit skill-set overlap matching (separate from, but combined with, text similarity)
- An estimated, component-explained ATS compatibility score
- Skill-gap prioritization based on job-description mention frequency
- Personalized, user-scoped analysis history across multiple resume submissions over time

This project does **not** claim that this combination automatically qualifies for a
patent or other formal intellectual property protection. It is presented here as
technical documentation describing what was built and how, for the purpose of potential
future evaluation.

## 8. Future IP Evaluation

Patentability and legal protection should be evaluated by a qualified intellectual-property
professional based on applicable laws and prior-art searches. This document does not
constitute legal advice and no claims of patent-pending or registered IP status are made
by this project or its author unless and until such registration is formally obtained.
