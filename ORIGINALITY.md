# Project Originality

## Problem Addressed

Students and job seekers frequently struggle to understand whether their resume is well
structured, whether it would pass an automated screening step, and how well it aligns with
a specific job description. Manually comparing a resume against a job posting to identify
missing skills and keywords is slow, inconsistent, and easy to get wrong.

## Proposed Solution

This project implements a self-contained pipeline that:

1. Extracts resume text from PDF/DOCX/TXT files.
2. Detects the presence or absence of standard resume sections.
3. Extracts recognized skills/keywords using a curated local skills database.
4. Computes an explainable, component-based "Estimated ATS Compatibility Score."
5. Compares the resume against a user-provided job description using TF-IDF cosine
   similarity combined with explicit skill-set overlap.
6. Identifies skill gaps and assigns a learning priority based on how often each missing
   skill is mentioned in the job description.
7. Generates specific, non-generic resume improvement suggestions derived directly from
   the detected issues.
8. Persists each user's analysis history in a per-user, access-controlled manner.

## System Workflow

```
Resume Upload -> Text Extraction -> Text Cleaning -> Section Detection ->
Skill & Keyword Extraction -> Job Description Processing -> TF-IDF/Similarity Analysis ->
Skill Matching -> ATS Compatibility Calculation -> Skill Gap Identification ->
Recommendations -> Save to Analysis History -> Streamlit Dashboard
```

## NLP Methodology

- Regex-based text cleaning and tokenization with a custom stopword list.
- Word-boundary regex matching against a structured skills database for skill extraction
  (avoids false positives, e.g. matching "R" inside "Random").
- Heuristic detection of generic phrases, repeated words, and measurable achievements
  (numeric/percentage patterns near achievement verbs).

## ML Methodology

- TF-IDF (Term Frequency–Inverse Document Frequency) vectorization of resume and job
  description text using scikit-learn.
- Cosine similarity between the two TF-IDF vectors as a quantitative measure of textual
  relevance between resume and job description.

## ATS Scoring Methodology

A four-component, equally-weighted (25 points each) scoring model:
Structure & Section Completeness, Skills Relevance, Text Quality, and Job Description
Match. Each component's contribution is shown to the user with a plain-language
explanation, rather than presented as an opaque single number.

## Skill Matching Approach

Skills are extracted independently from both the resume and the job description using the
same local skills database, then compared as sets to compute matched/missing skills and a
skill overlap ratio, which is combined with TF-IDF similarity for the final job match score.

## Skill Gap Detection Approach

Missing skills (present in the JD, absent from the resume) are ranked by a simple,
explainable proxy for importance: the number of times each skill is mentioned in the job
description text.

## User-Specific Analysis History

Each registered user's analyses are stored in a SQLite database, scoped by `user_id`, with
application-level checks ensuring a user can only read their own analysis records.

## Overall System Architecture

A modular Python/Streamlit application, with clearly separated concerns: parsing,
NLP/text processing, scoring, matching, database access, authentication, and reporting —
each implemented as an independent module under `modules/`.

---

## Original Components

The following components were specifically designed and implemented for this project
(as opposed to being off-the-shelf libraries or generic techniques):

1. **Resume analysis pipeline** — the specific sequence and combination of parsing,
   section detection, skill extraction, scoring, and recommendation steps.
2. **Estimated ATS scoring methodology** — the specific four-component weighting model
   and its component-level explanations.
3. **Resume-to-job skill matching logic** — the combination formula
   (60% skill overlap + 40% TF-IDF similarity) used for the Job Match Percentage.
4. **Skill gap prioritization logic** — the mention-frequency-based priority assignment.
5. **Keyword recommendation logic** — category-grouped missing keyword identification
   with an explicit "only add skills you genuinely have" caution.
6. **Personalized analysis dashboard** — the specific set of metrics and history view
   presented to each user.
7. **Analysis history system** — the per-user, access-controlled storage and retrieval
   of past analyses.

## What Is Not Claimed as Original

This project does **not** claim that the following generic technologies or well-known
techniques were invented by the project:

- Python, Streamlit, SQLite, or any third-party library used
- TF-IDF vectorization or cosine similarity as general NLP/ML techniques
- bcrypt password hashing
- Standard software engineering patterns (MVC-style module separation, session-based auth)

The originality claimed is in the **specific combination, weighting, and implementation**
of these general-purpose techniques into this particular resume-analysis system — not in
the underlying techniques themselves.
