"""
skill_gap.py
------------
Divides skills into "Already Have", "Missing / Skill Gap" and assigns
a learning priority based on frequency of mention in the job description
(a simple, explainable proxy for importance/relevance).
"""

import re
from modules.skill_extractor import load_skills_database, extract_skills_flat


def _count_mentions(skill: str, text: str) -> int:
    pattern = r"(?<![A-Za-z0-9])" + re.escape(skill) + r"(?![A-Za-z0-9])"
    return len(re.findall(pattern, text, re.IGNORECASE))


def analyze_skill_gap(resume_text: str, jd_text: str) -> dict:
    """
    Returns:
      already_have: list of skills present in both
      missing: list of dicts {skill, priority} for JD skills not in resume
    Priority is based on how many times the skill is mentioned in the JD:
      3+ mentions -> High, 2 mentions -> Medium, 1 mention -> Low
    """
    if not jd_text or not jd_text.strip():
        return {"already_have": [], "missing": [], "note": "No job description provided."}

    skills_df = load_skills_database()
    resume_skills = set(extract_skills_flat(resume_text, skills_df))
    jd_skills = set(extract_skills_flat(jd_text, skills_df))

    already_have = sorted(resume_skills & jd_skills)
    gap_skills = jd_skills - resume_skills

    missing = []
    for skill in gap_skills:
        mentions = _count_mentions(skill, jd_text)
        if mentions >= 3:
            priority = "High Priority"
        elif mentions == 2:
            priority = "Medium Priority"
        else:
            priority = "Low Priority"
        missing.append({"skill": skill, "mentions_in_jd": mentions, "priority": priority})

    priority_order = {"High Priority": 0, "Medium Priority": 1, "Low Priority": 2}
    missing.sort(key=lambda x: priority_order[x["priority"]])

    return {
        "already_have": already_have,
        "missing": missing,
        "note": "Priority is based on how frequently each skill is mentioned in the job description.",
    }
