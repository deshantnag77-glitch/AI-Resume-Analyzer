"""
section_detector.py
--------------------
Detects which standard resume sections are present, using heading
keyword matching against the raw (non-lowercased-only) resume text.
"""

import re

SECTION_KEYWORDS = {
    "Contact Information": [
        r"email", r"phone", r"contact", r"linkedin", r"github",
        r"@\w+\.\w+", r"\+?\d{10}",
    ],
    "Career Objective / Summary": [
        r"career objective", r"summary", r"professional summary",
        r"objective", r"profile summary", r"about me",
    ],
    "Education": [
        r"education", r"academic", r"qualification", r"b\.?tech",
        r"bachelor", r"university", r"college", r"cgpa", r"percentage",
    ],
    "Skills": [
        r"skills", r"technical skills", r"core competencies",
        r"technologies", r"proficiencies",
    ],
    "Projects": [
        r"projects", r"academic projects", r"personal projects",
    ],
    "Experience": [
        r"experience", r"work experience", r"employment history",
        r"professional experience",
    ],
    "Certifications": [
        r"certification", r"certificate", r"licenses",
    ],
    "Achievements": [
        r"achievements", r"awards", r"honors", r"accomplishments",
    ],
    "Internships": [
        r"internship", r"intern\b", r"training",
    ],
}


def detect_sections(resume_text: str) -> dict:
    """
    Returns a dict: {section_name: True/False} indicating whether
    evidence of that section heading/content was found in the resume.
    """
    text_lower = resume_text.lower()
    results = {}

    for section, patterns in SECTION_KEYWORDS.items():
        found = any(re.search(pattern, text_lower) for pattern in patterns)
        results[section] = found

    return results


def get_missing_sections(section_results: dict) -> list:
    return [section for section, present in section_results.items() if not present]


def get_present_sections(section_results: dict) -> list:
    return [section for section, present in section_results.items() if present]


def section_completeness_score(section_results: dict) -> float:
    """Fraction (0-1) of standard sections present."""
    if not section_results:
        return 0.0
    present = sum(1 for v in section_results.values() if v)
    return present / len(section_results)
