"""
database.py
------------
SQLite database setup and access functions for users, profiles and
analysis history. Kept deliberately simple for a college VT project.
"""

import sqlite3
import os
import json
from datetime import datetime

DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database")
DB_PATH = os.path.join(DB_DIR, "resume_analyzer.db")


def get_connection():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            user_id INTEGER PRIMARY KEY,
            education TEXT,
            branch TEXT,
            graduation_year TEXT,
            target_role TEXT,
            preferred_domain TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            resume_filename TEXT,
            ats_score REAL,
            job_match_score REAL,
            result_json TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS analysis_skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            analysis_id INTEGER NOT NULL,
            skill TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (analysis_id) REFERENCES analyses (id) ON DELETE CASCADE
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            user_id INTEGER PRIMARY KEY,
            target_job_role TEXT,
            preferred_industry TEXT,
            matching_strictness TEXT DEFAULT 'Medium',
            min_keyword_relevance INTEGER DEFAULT 50,
            theme TEXT DEFAULT 'Light',
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


# ---------- USER FUNCTIONS ----------

def create_user(name: str, email: str, password_hash: str) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (name, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
        (name, email.lower().strip(), password_hash, datetime.now().isoformat()),
    )
    user_id = cur.lastrowid
    cur.execute("INSERT INTO user_profiles (user_id) VALUES (?)", (user_id,))
    cur.execute("INSERT INTO settings (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()
    return user_id


def get_user_by_email(email: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email.lower().strip(),))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_by_id(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def update_user_password(user_id: int, new_hash: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, user_id))
    conn.commit()
    conn.close()


def update_user_basic(user_id: int, name: str, email: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email.lower().strip(), user_id))
    conn.commit()
    conn.close()


def delete_user(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = ?", (user_id,))  # cascades
    conn.commit()
    conn.close()


# ---------- PROFILE FUNCTIONS ----------

def get_profile(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM user_profiles WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def update_profile(user_id: int, education, branch, graduation_year, target_role, preferred_domain):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE user_profiles
        SET education = ?, branch = ?, graduation_year = ?, target_role = ?, preferred_domain = ?
        WHERE user_id = ?
    """, (education, branch, graduation_year, target_role, preferred_domain, user_id))
    conn.commit()
    conn.close()


# ---------- SETTINGS FUNCTIONS ----------

def get_settings(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM settings WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def update_settings(user_id: int, target_job_role, preferred_industry, matching_strictness, min_keyword_relevance, theme):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE settings
        SET target_job_role = ?, preferred_industry = ?, matching_strictness = ?,
            min_keyword_relevance = ?, theme = ?
        WHERE user_id = ?
    """, (target_job_role, preferred_industry, matching_strictness, min_keyword_relevance, theme, user_id))
    conn.commit()
    conn.close()


# ---------- ANALYSIS FUNCTIONS ----------

def save_analysis(user_id: int, resume_filename: str, ats_score: float,
                   job_match_score, result_dict: dict, matched_skills=None, missing_skills=None) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO analyses (user_id, resume_filename, ats_score, job_match_score, result_json, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, resume_filename, ats_score, job_match_score, json.dumps(result_dict), datetime.now().isoformat()))
    analysis_id = cur.lastrowid

    for skill in (matched_skills or []):
        cur.execute("INSERT INTO analysis_skills (analysis_id, skill, status) VALUES (?, ?, ?)",
                     (analysis_id, skill, "matched"))
    for skill in (missing_skills or []):
        cur.execute("INSERT INTO analysis_skills (analysis_id, skill, status) VALUES (?, ?, ?)",
                     (analysis_id, skill, "missing"))

    conn.commit()
    conn.close()
    return analysis_id


def get_user_analyses(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM analyses WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_analysis_by_id(analysis_id: int, user_id: int):
    """user_id check ensures users can only access their own analyses."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM analyses WHERE id = ? AND user_id = ?", (analysis_id, user_id))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def clear_user_history(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM analyses WHERE user_id = ?", (user_id,))  # cascades to analysis_skills
    conn.commit()
    conn.close()
