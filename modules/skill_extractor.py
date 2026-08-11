"""
skill_extractor.py
-------------------
Extracts known skills/technologies from a piece of text by matching
against the local skills database (data/skills.csv). Uses word-boundary
regex matching so "R" doesn't match inside "Random", etc.
"""

import re
import os
import pandas as pd

SKILLS_CSV_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "skills.csv"
)


def load_skills_database() -> pd.DataFrame:
    df = pd.read_csv(SKILLS_CSV_PATH)
    return df


def _build_pattern(skill: str) -> re.Pattern:
    """Build a safe, case-insensitive, word-boundary regex for a skill name."""
    escaped = re.escape(skill)
    # Allow "C++" and "C#" style tokens; escape already handles special chars.
    pattern = r"(?<![A-Za-z0-9])" + escaped + r"(?![A-Za-z0-9])"
    return re.compile(pattern, re.IGNORECASE)


def extract_skills(text: str, skills_df: pd.DataFrame = None) -> dict:
    """
    Scans text for known skills.
    Returns dict: {category: [skills found]}
    """
    if skills_df is None:
        skills_df = load_skills_database()

    found = {}
    for _, row in skills_df.iterrows():
        skill = row["skill"]
        category = row["category"]
        pattern = _build_pattern(skill)
        if pattern.search(text):
            found.setdefault(category, [])
            if skill not in found[category]:
                found[category].append(skill)

    return found


def flatten_skills(skills_by_category: dict) -> list:
    """Flatten the category dict into a single sorted list of skill names."""
    all_skills = []
    for skills in skills_by_category.values():
        all_skills.extend(skills)
    return sorted(set(all_skills))


def extract_skills_flat(text: str, skills_df: pd.DataFrame = None) -> list:
    return flatten_skills(extract_skills(text, skills_df))
