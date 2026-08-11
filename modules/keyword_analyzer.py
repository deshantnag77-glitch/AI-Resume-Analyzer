"""
keyword_analyzer.py
--------------------
Identifies keywords present in the job description but missing from the
resume, grouped by category using the local skills database.
"""

from modules.skill_extractor import load_skills_database, extract_skills


def analyze_keywords(resume_text: str, jd_text: str) -> dict:
    """
    Returns missing keywords grouped by category, plus a caution note.
    If no JD is given, returns an empty structure.
    """
    if not jd_text or not jd_text.strip():
        return {"by_category": {}, "note": "No job description provided."}

    skills_df = load_skills_database()
    resume_by_cat = extract_skills(resume_text, skills_df)
    jd_by_cat = extract_skills(jd_text, skills_df)

    resume_flat = set()
    for skills in resume_by_cat.values():
        resume_flat.update(skills)

    missing_by_category = {}
    for category, jd_skills in jd_by_cat.items():
        missing = [s for s in jd_skills if s not in resume_flat]
        if missing:
            missing_by_category[category] = missing

    return {
        "by_category": missing_by_category,
        "note": "Only add skills you genuinely know or have used. "
                "Do not add a keyword without real experience or knowledge of it.",
    }
