"""
job_matcher.py
---------------
Compares resume text against a job description using TF-IDF vectorization
and cosine similarity. This is a real, explainable NLP similarity method
(not a random or hardcoded score).
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from modules.text_processor import clean_text
from modules.skill_extractor import extract_skills_flat, load_skills_database


def compute_similarity(resume_text: str, jd_text: str) -> float:
    """
    Computes TF-IDF cosine similarity between resume and job description.
    Returns a percentage (0-100).
    """
    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(jd_text)

    if not resume_clean or not jd_clean:
        return 0.0

    vectorizer = TfidfVectorizer(stop_words="english")
    try:
        tfidf_matrix = vectorizer.fit_transform([resume_clean, jd_clean])
    except ValueError:
        # Happens if both documents contain only stopwords/empty vocab
        return 0.0

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(float(similarity) * 100, 2)


def match_skills(resume_text: str, jd_text: str) -> dict:
    """
    Compares extracted skills between resume and job description.
    Returns matched skills, missing skills, and match ratio.
    """
    skills_df = load_skills_database()
    resume_skills = set(extract_skills_flat(resume_text, skills_df))
    jd_skills = set(extract_skills_flat(jd_text, skills_df))

    matched = sorted(resume_skills & jd_skills)
    missing = sorted(jd_skills - resume_skills)
    extra = sorted(resume_skills - jd_skills)

    if jd_skills:
        skill_match_ratio = round((len(matched) / len(jd_skills)) * 100, 2)
    else:
        skill_match_ratio = 0.0

    return {
        "resume_skills": sorted(resume_skills),
        "jd_skills": sorted(jd_skills),
        "matched_skills": matched,
        "missing_skills": missing,
        "extra_skills": extra,
        "skill_match_ratio": skill_match_ratio,
    }


def compute_job_match(resume_text: str, jd_text: str) -> dict:
    """
    Full job matching pipeline combining TF-IDF text similarity
    with explicit skill-set matching for a more explainable result.

    Final Job Match % = 60% skill overlap + 40% TF-IDF text similarity
    (weights are documented and explainable, not arbitrary black-box output)
    """
    if not jd_text or not jd_text.strip():
        return None

    text_similarity = compute_similarity(resume_text, jd_text)
    skill_data = match_skills(resume_text, jd_text)

    final_score = round(
        (0.6 * skill_data["skill_match_ratio"]) + (0.4 * text_similarity), 2
    )
    final_score = min(final_score, 100.0)

    return {
        "text_similarity": text_similarity,
        "skill_match_ratio": skill_data["skill_match_ratio"],
        "job_match_percentage": final_score,
        "matched_skills": skill_data["matched_skills"],
        "missing_skills": skill_data["missing_skills"],
        "resume_skills": skill_data["resume_skills"],
        "jd_skills": skill_data["jd_skills"],
    }
