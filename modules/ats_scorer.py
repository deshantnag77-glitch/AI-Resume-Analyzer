"""
ats_scorer.py
-------------
Computes an "Estimated ATS Compatibility Score" out of 100, broken into
four explainable components. This is NOT a claim of matching any real
commercial ATS vendor's proprietary algorithm — it is a heuristic,
transparent scoring model built for this project.

Components (each out of 25):
  1. Structure / Section Completeness  -> section_detector results
  2. Keyword & Skills Relevance        -> skills found relative to expectation
  3. Text Quality                      -> length, repetition, measurable results
  4. Job-Description Match (if provided) -> falls back to skill richness if no JD
"""

from modules.section_detector import detect_sections, section_completeness_score
from modules.skill_extractor import extract_skills_flat
from modules.text_processor import (
    word_count,
    detect_repeated_words,
    detect_generic_phrases,
    has_measurable_achievements,
)
from modules.job_matcher import compute_job_match


def score_structure(resume_text: str) -> dict:
    """Section completeness -> out of 25."""
    sections = detect_sections(resume_text)
    completeness = section_completeness_score(sections)
    score = round(completeness * 25, 1)
    return {
        "score": score,
        "max": 25,
        "sections": sections,
        "explanation": f"{sum(sections.values())} of {len(sections)} standard resume sections detected.",
    }


def score_skills(resume_text: str) -> dict:
    """Skill richness -> out of 25. Based on breadth of recognized skills."""
    skills = extract_skills_flat(resume_text)
    # Heuristic: 10+ distinct recognized skills = full marks, scaled linearly below that.
    target = 10
    ratio = min(len(skills) / target, 1.0)
    score = round(ratio * 25, 1)
    return {
        "score": score,
        "max": 25,
        "skills_found": skills,
        "explanation": f"{len(skills)} recognized technical/soft skills found (target: {target}+).",
    }


def score_text_quality(resume_text: str) -> dict:
    """Text quality -> out of 25. Penalizes weak/short/repetitive/generic content."""
    score = 25.0
    issues = []

    wc = word_count(resume_text)
    if wc < 150:
        score -= 10
        issues.append("Resume content is quite short; add more detail to projects/experience.")
    elif wc < 250:
        score -= 5
        issues.append("Resume content is somewhat short.")

    repeated = detect_repeated_words(resume_text)
    if repeated:
        score -= 5
        top_words = ", ".join(w for w, c in repeated[:3])
        issues.append(f"Some words are repeated often ({top_words}); vary your language.")

    generic = detect_generic_phrases(resume_text)
    if generic:
        score -= 5
        issues.append(f"Generic phrases found ({', '.join(generic[:3])}); replace with specific examples.")

    if not has_measurable_achievements(resume_text):
        score -= 5
        issues.append("No measurable achievements detected (numbers, %, quantified results).")

    score = max(score, 0.0)
    return {
        "score": round(score, 1),
        "max": 25,
        "issues": issues,
        "explanation": "Based on length, repetition, generic phrasing and measurable achievements.",
    }


def score_job_match_component(resume_text: str, jd_text: str) -> dict:
    """
    Job-description match -> out of 25.
    If no JD is provided, this component falls back to a neutral
    mid-range score based on skill breadth only, and is labeled as such.
    """
    if jd_text and jd_text.strip():
        match_data = compute_job_match(resume_text, jd_text)
        score = round((match_data["job_match_percentage"] / 100) * 25, 1)
        return {
            "score": score,
            "max": 25,
            "explanation": f"Based on {match_data['job_match_percentage']}% job description match.",
            "used_jd": True,
        }
    else:
        # No JD provided: give a neutral estimate based on skill count alone.
        skills = extract_skills_flat(resume_text)
        ratio = min(len(skills) / 10, 1.0)
        score = round(ratio * 25 * 0.75, 1)  # slightly conservative without JD context
        return {
            "score": score,
            "max": 25,
            "explanation": "No job description provided — estimated from general skill breadth only. "
                            "Paste a job description for a more accurate score.",
            "used_jd": False,
        }


def compute_ats_score(resume_text: str, jd_text: str = "") -> dict:
    """
    Master function combining all four components into a final
    Estimated ATS Compatibility Score (0-100).
    """
    structure = score_structure(resume_text)
    skills = score_skills(resume_text)
    quality = score_text_quality(resume_text)
    job_match = score_job_match_component(resume_text, jd_text)

    total = round(
        structure["score"] + skills["score"] + quality["score"] + job_match["score"], 1
    )

    if total >= 80:
        rating = "Strong"
    elif total >= 60:
        rating = "Good"
    elif total >= 40:
        rating = "Needs Improvement"
    else:
        rating = "Weak"

    return {
        "total_score": total,
        "rating": rating,
        "components": {
            "Structure & Section Completeness": structure,
            "Skills Relevance": skills,
            "Text Quality": quality,
            "Job Description Match": job_match,
        },
    }
