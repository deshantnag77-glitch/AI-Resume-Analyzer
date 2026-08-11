"""
suggestions.py
---------------
Generates practical, specific resume improvement suggestions based on
the actual analysis results (not generic motivational text).
"""

from modules.section_detector import get_missing_sections


SECTION_SUGGESTIONS = {
    "Contact Information": "Add your email, phone number and LinkedIn/GitHub link at the top of the resume.",
    "Career Objective / Summary": "Add a 2-3 line professional summary stating your target role and key strengths.",
    "Education": "Add your degree, institution name, graduation year and CGPA/percentage.",
    "Skills": "Add a dedicated Skills section listing your technical and relevant soft skills.",
    "Projects": "Add the technologies used, your specific contribution, and the measurable result of each project.",
    "Experience": "Add your role, company, duration, and 2-3 bullet points describing your impact.",
    "Certifications": "List relevant certifications with the issuing platform/organization and date.",
    "Achievements": "Add academic or extracurricular achievements with specific, quantifiable details.",
    "Internships": "Add internship details including organization, duration, and key contributions.",
}


def generate_suggestions(section_results: dict, quality_issues: list, job_match_data: dict = None) -> list:
    """
    Combines section-based, quality-based and job-match-based suggestions
    into one prioritized, deduplicated list.
    """
    suggestions = []

    missing_sections = get_missing_sections(section_results)
    for section in missing_sections:
        suggestions.append(SECTION_SUGGESTIONS.get(section, f"Add a {section} section."))

    suggestions.extend(quality_issues)

    if job_match_data and job_match_data.get("missing_skills"):
        top_missing = job_match_data["missing_skills"][:5]
        suggestions.append(
            "Consider learning/adding these job-relevant skills if you genuinely have experience with them: "
            + ", ".join(top_missing)
        )

    # Deduplicate while preserving order
    seen = set()
    unique_suggestions = []
    for s in suggestions:
        if s not in seen:
            seen.add(s)
            unique_suggestions.append(s)

    return unique_suggestions
