"""
app.py
------
AI Resume Analyzer & Job Matcher
Main Streamlit application entry point.

Technology: Python | NLP | Machine Learning | Streamlit | SQLite
"""

import streamlit as st
import pandas as pd
from datetime import datetime

import database as db
import auth

from modules.resume_parser import parse_resume, ResumeParseError
from modules.section_detector import (
    detect_sections,
    get_missing_sections,
    get_present_sections,
)
from modules.skill_extractor import extract_skills, extract_skills_flat
from modules.ats_scorer import compute_ats_score
from modules.job_matcher import compute_job_match
from modules.keyword_analyzer import analyze_keywords
from modules.skill_gap import analyze_skill_gap
from modules.suggestions import generate_suggestions
from modules.report_generator import generate_pdf_report
from modules.text_processor import (
    detect_repeated_words,
    detect_generic_phrases,
    has_measurable_achievements,
    word_count,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Resume Analyzer & Job Matcher",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# RESPONSIVE LIGHT THEME
# ============================================================

CUSTOM_CSS = """
<style>

/* ==========================================================
   GLOBAL
========================================================== */

html, body {
    background-color: #ffffff !important;
}

.stApp {
    background-color: #ffffff !important;
}

.main {
    background-color: #ffffff !important;
}

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
}


/* ==========================================================
   TEXT
========================================================== */

h1,
h2,
h3,
h4,
h5,
h6 {
    color: #111111 !important;
    font-weight: 700 !important;
}

p,
li,
span,
label {
    color: #222222 !important;
}

[data-testid="stMarkdownContainer"] {
    color: #222222 !important;
}

[data-testid="stCaptionContainer"] {
    color: #555555 !important;
}


/* ==========================================================
   SIDEBAR
========================================================== */

section[data-testid="stSidebar"] {
    background-color: #f7f8fa !important;
    border-right: 1px solid #dddddd !important;
}

section[data-testid="stSidebar"] * {
    color: #111111 !important;
}

section[data-testid="stSidebar"] .stRadio label {
    color: #111111 !important;
    font-weight: 500 !important;
}


/* ==========================================================
   TEXT INPUT
========================================================== */

.stTextInput label,
.stTextArea label,
.stSelectbox label,
.stFileUploader label,
.stSlider label,
.stRadio label,
.stCheckbox label {
    color: #111111 !important;
    font-weight: 600 !important;
}

.stTextInput input,
.stTextArea textarea {
    background-color: #ffffff !important;
    color: #111111 !important;
    border: 1px solid #b8b8b8 !important;
    border-radius: 9px !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 1px #2563eb !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #777777 !important;
    opacity: 1 !important;
}


/* ==========================================================
   FILE UPLOADER
========================================================== */

[data-testid="stFileUploader"] {
    background-color: #f8fbff !important;
    border: 2px dashed #2563eb !important;
    border-radius: 12px !important;
    padding: 14px !important;
}

[data-testid="stFileUploader"] * {
    color: #111111 !important;
}

[data-testid="stFileUploaderDropzone"] {
    background-color: #f8fbff !important;
}


/* ==========================================================
   BUTTONS
========================================================== */

.stButton > button,
.stFormSubmitButton > button,
.stDownloadButton > button {
    background-color: #2563eb !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 9px !important;
    min-height: 42px !important;
    font-weight: 600 !important;
}

.stButton > button *,
.stFormSubmitButton > button *,
.stDownloadButton > button * {
    color: #ffffff !important;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover,
.stDownloadButton > button:hover {
    background-color: #1d4ed8 !important;
}


/* ==========================================================
   METRIC CARD
========================================================== */

.metric-card {
    background-color: #ffffff !important;
    border: 1px solid #dddddd !important;
    border-radius: 12px !important;
    padding: 20px !important;
    text-align: center !important;
    margin-bottom: 10px !important;
}

.metric-card h2 {
    margin: 0 !important;
    color: #2563eb !important;
    font-size: 28px !important;
}

.metric-card p {
    margin-top: 5px !important;
    color: #555555 !important;
}


/* ==========================================================
   EXPANDER
========================================================== */

[data-testid="stExpander"] {
    background-color: #ffffff !important;
    border: 1px solid #dddddd !important;
    border-radius: 10px !important;
}

[data-testid="stExpander"] * {
    color: #222222 !important;
}


/* ==========================================================
   SELECTBOX
========================================================== */

[data-baseweb="select"] {
    background-color: #ffffff !important;
}

[data-baseweb="select"] * {
    color: #111111 !important;
}


/* ==========================================================
   ALERTS
========================================================== */

[data-testid="stAlert"] {
    border-radius: 9px !important;
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] span {
    color: #222222 !important;
}


/* ==========================================================
   TABLE
========================================================== */

[data-testid="stDataFrame"] {
    background-color: #ffffff !important;
}

[data-testid="stDataFrame"] * {
    color: #222222 !important;
}


/* ==========================================================
   UPLOAD INFORMATION BOX
========================================================== */

.upload-info {
    background-color: #f5f8fc !important;
    border: 1px solid #dce6f2 !important;
    border-radius: 10px !important;
    padding: 14px 16px !important;
    margin-bottom: 12px !important;
}

.upload-info,
.upload-info * {
    color: #222222 !important;
}


/* ==========================================================
   CODE / TEXT PREVIEW
========================================================== */

pre,
code {
    background-color: #f4f4f4 !important;
    color: #222222 !important;
}


/* ==========================================================
   MOBILE RESPONSIVE
========================================================== */

@media (max-width: 768px) {

    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-top: 1rem !important;
    }

    h1 {
        font-size: 28px !important;
    }

    h2 {
        font-size: 24px !important;
    }

    h3 {
        font-size: 20px !important;
    }

    p {
        font-size: 15px !important;
    }

    .metric-card {
        padding: 15px !important;
    }

    .metric-card h2 {
        font-size: 24px !important;
    }

    .stButton > button,
    .stFormSubmitButton > button,
    .stDownloadButton > button {
        width: 100% !important;
        min-height: 45px !important;
    }

    .stTextArea textarea {
        min-height: 220px !important;
    }

    [data-testid="stFileUploader"] {
        padding: 10px !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #f7f8fa !important;
    }
}


    /* FILE UPLOADER FIX */
    [data-testid="stFileUploader"] {
        color: #222222 !important;
    }

    [data-testid="stFileUploader"] section {
        background-color: #ffffff !important;
        border: 2px dashed #1e5aa8 !important;
        border-radius: 10px !important;
    }

    [data-testid="stFileUploader"] section * {
        color: #222222 !important;
    }

    [data-testid="stFileUploader"] button {
        background-color: #1e5aa8 !important;
        color: #ffffff !important;
        border: none !important;
    }

    [data-testid="stFileUploader"] button * {
        color: #ffffff !important;
    }

    [data-testid="stFileUploader"] small {
        color: #555555 !important;
    }

</style>
"""

st.markdown(
    CUSTOM_CSS,
    unsafe_allow_html=True
)


# ============================================================
# DATABASE INIT
# ============================================================

db.init_db()


# ============================================================
# SESSION STATE
# ============================================================

if "user" not in st.session_state:
    st.session_state.user = None

if "auth_page" not in st.session_state:
    st.session_state.auth_page = "login"

if "current_analysis" not in st.session_state:
    st.session_state.current_analysis = None

if "viewing_history_id" not in st.session_state:
    st.session_state.viewing_history_id = None


# ============================================================
# LOGOUT
# ============================================================

def logout():

    st.session_state.user = None
    st.session_state.current_analysis = None
    st.session_state.viewing_history_id = None
    st.session_state.auth_page = "login"


# ============================================================
# LOGIN
# ============================================================

def render_login_page():

    st.markdown(
        "## AI Resume Analyzer & Job Matcher"
    )

    st.caption(
        "AI-powered Resume Analysis, ATS Score Checking "
        "and Job Skill Matching System"
    )

    st.markdown("---")

    col1, col2 = st.columns(
        [1, 1]
    )

    with col1:

        st.markdown("### Login")

        with st.form("login_form"):

            email = st.text_input(
                "Email",
                placeholder="Enter your email"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password"
            )

            remember = st.checkbox(
                "Remember Me",
                value=True
            )

            submitted = st.form_submit_button(
                "Login"
            )

            if submitted:

                try:

                    user = auth.login_user(
                        email,
                        password
                    )

                    st.session_state.user = user

                    st.success(
                        f"Welcome back, {user['name']}!"
                    )

                    st.rerun()

                except auth.AuthError as e:

                    st.error(
                        str(e)
                    )

        st.caption(
            "Forgot Password? Contact the system administrator "
            "(demo project - reset flow not implemented)."
        )

        if st.button(
            "Create an Account"
        ):

            st.session_state.auth_page = "register"
            st.rerun()

    with col2:

        st.markdown(
            "### About this project"
        )

        st.write(
            "This is a Python-based NLP and Machine Learning "
            "application that helps students and job seekers "
            "analyze their resumes, estimate ATS compatibility, "
            "and compare their skills against a job description."
        )

        st.write(
            "**Technology used:** Python, NLP, "
            "Machine Learning, Streamlit, SQLite"
        )


# ============================================================
# REGISTER
# ============================================================

def render_register_page():

    st.markdown(
        "## Create Account"
    )

    st.markdown("---")

    with st.form(
        "register_form"
    ):

        name = st.text_input(
            "Full Name",
            placeholder="Enter your full name"
        )

        email = st.text_input(
            "Email",
            placeholder="Enter your email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Confirm password"
        )

        submitted = st.form_submit_button(
            "Register"
        )

        if submitted:

            try:

                user = auth.register_user(
                    name,
                    email,
                    password,
                    confirm_password
                )

                st.success(
                    "Account created successfully. Please log in."
                )

                st.session_state.auth_page = "login"
                st.rerun()

            except auth.AuthError as e:

                st.error(
                    str(e)
                )

    if st.button(
        "Back to Login"
    ):

        st.session_state.auth_page = "login"
        st.rerun()


# ============================================================
# ANALYSIS PIPELINE
# ============================================================

def run_full_analysis(
    resume_text: str,
    jd_text: str
) -> dict:

    sections = detect_sections(
        resume_text
    )

    ats_result = compute_ats_score(
        resume_text,
        jd_text
    )

    job_match_result = (
        compute_job_match(
            resume_text,
            jd_text
        )
        if jd_text.strip()
        else None
    )

    keyword_result = analyze_keywords(
        resume_text,
        jd_text
    )

    skill_gap_result = analyze_skill_gap(
        resume_text,
        jd_text
    )

    quality_issues = ats_result[
        "components"
    ][
        "Text Quality"
    ][
        "issues"
    ]

    suggestions = generate_suggestions(
        sections,
        quality_issues,
        job_match_result
    )

    resume_skills_by_cat = extract_skills(
        resume_text
    )

    return {

        "resume_text":
            resume_text,

        "jd_text":
            jd_text,

        "sections":
            sections,

        "ats_result":
            ats_result,

        "job_match_result":
            job_match_result,

        "keyword_result":
            keyword_result,

        "skill_gap_result":
            skill_gap_result,

        "suggestions":
            suggestions,

        "resume_skills_by_cat":
            resume_skills_by_cat,

        "timestamp":
            datetime.now().isoformat(),
    }


# ============================================================
# DASHBOARD
# ============================================================

def page_dashboard():

    user = st.session_state.user

    st.markdown(
        f"## Welcome, {user['name']}"
    )

    st.caption(
        "Analyze your resume. Match your skills. "
        "Improve your chances."
    )

    st.markdown("---")

    analyses = db.get_user_analyses(
        user["id"]
    )

    total = len(
        analyses
    )

    avg_ats = (
        round(
            sum(
                a["ats_score"] or 0
                for a in analyses
            ) / total,
            1
        )
        if total
        else 0
    )

    best_match = max(
        (
            a["job_match_score"] or 0
            for a in analyses
        ),
        default=0
    )

    all_missing = 0

    for a in analyses:

        conn = db.get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT COUNT(*) as c
            FROM analysis_skills
            WHERE analysis_id = ?
            AND status = 'missing'
            """,
            (a["id"],)
        )

        all_missing += cur.fetchone()["c"]

        conn.close()

    c1, c2, c3, c4 = st.columns(
        4
    )

    values = [
        total,
        f"{avg_ats}/100",
        f"{best_match}%",
        all_missing
    ]

    labels = [
        "Resumes Analyzed",
        "Average ATS Score",
        "Best Job Match",
        "Skill Gaps Identified"
    ]

    for col, value, label in zip(
        [c1, c2, c3, c4],
        values,
        labels
    ):

        col.markdown(
            f"""
            <div class="metric-card">
                <h2>{value}</h2>
                <p>{label}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        "### Recent Analysis"
    )

    if analyses:

        table_rows = []

        for a in analyses[:10]:

            table_rows.append(
                {
                    "Resume":
                        a["resume_filename"] or "N/A",

                    "ATS Score":
                        a["ats_score"],

                    "Job Match":
                        (
                            f"{a['job_match_score']}%"
                            if a["job_match_score"] is not None
                            else "N/A"
                        ),

                    "Date":
                        a["created_at"][:16].replace(
                            "T",
                            " "
                        ),
                }
            )

        df = pd.DataFrame(
            table_rows
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "Open Analysis History from the sidebar "
            "to view full details or download a report."
        )

    else:

        st.info(
            "No resumes analyzed yet. "
            "Go to Resume Analyzer to get started."
        )


# ============================================================
# RESUME ANALYZER
# ============================================================

def page_resume_analyzer():

    st.markdown(
        "## Resume Analyzer"
    )

    st.caption(
        "Upload your resume and optionally paste a job "
        "description for full analysis."
    )

    st.markdown("---")

    # --------------------------------------------------------
    # UPLOAD
    # --------------------------------------------------------

    st.markdown(
        "### 📄 Upload Resume"
    )

    st.markdown(
        """
        <div class="upload-info">
        <b>Supported formats:</b>
        PDF • DOCX • TXT
        <br><br>
        <b>TXT resumes are fully supported.</b>
        You can upload a normal .txt resume directly.
        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Choose Resume File",
        type=[
            "pdf",
            "docx",
            "txt"
        ],
        help=(
            "Upload your resume as PDF, DOCX or TXT."
        )
    )

    if uploaded_file is not None:

        file_name = uploaded_file.name

        extension = (
            file_name
            .split(".")[-1]
            .lower()
        )

        if extension == "pdf":

            st.success(
                f"✅ PDF selected: {file_name}"
            )

        elif extension == "docx":

            st.success(
                f"✅ DOCX selected: {file_name}"
            )

        elif extension == "txt":

            st.success(
                f"✅ TXT selected: {file_name}"
            )

    # --------------------------------------------------------
    # JOB DESCRIPTION
    # --------------------------------------------------------

    st.markdown(
        "### 💼 Job Description"
    )

    jd_text = st.text_area(
        "Paste Job Description",
        height=220,
        placeholder=(
            "Paste the complete job description here...\n\n"
            "Example:\n"
            "We are looking for a Python Developer with "
            "knowledge of Python, SQL, Machine Learning, "
            "NLP, Git and REST APIs."
        ),
        help=(
            "Adding a job description enables Job Matcher, "
            "Keyword Suggestions and Skill Gap Analysis."
        )
    )

    # --------------------------------------------------------
    # ANALYZE
    # --------------------------------------------------------

    if st.button(
        "🔍 Analyze Resume",
        type="primary"
    ):

        if uploaded_file is None:

            st.error(
                "Please upload a resume file first."
            )

            return

        try:

            resume_text = parse_resume(
                uploaded_file
            )

        except ResumeParseError as e:

            st.error(
                str(e)
            )

            return

        except Exception as e:

            st.error(
                f"Unable to read the uploaded resume: {e}"
            )

            return

        if not resume_text.strip():

            st.error(
                "No readable text was found in this resume."
            )

            return

        with st.spinner(
            "Analyzing resume..."
        ):

            result = run_full_analysis(
                resume_text,
                jd_text
            )

            result["filename"] = (
                uploaded_file.name
            )

        st.session_state.current_analysis = (
            result
        )

        st.success(
            "✅ Analysis complete!"
        )

    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------

    if st.session_state.current_analysis:

        result = (
            st.session_state.current_analysis
        )

        st.markdown("---")

        st.markdown(
            "### 📋 Extracted Resume Preview"
        )

        with st.expander(
            "View extracted text"
        ):

            st.text(
                result["resume_text"][:5000]
            )

        st.markdown(
            "### 📑 Detected Sections"
        )

        present = get_present_sections(
            result["sections"]
        )

        missing = get_missing_sections(
            result["sections"]
        )

        col1, col2 = st.columns(
            2
        )

        with col1:

            st.markdown(
                "**Present:**"
            )

            for s in present:

                st.markdown(
                    f"- {s}"
                )

        with col2:

            st.markdown(
                "**Missing:**"
            )

            if missing:

                for s in missing:

                    st.markdown(
                        f"- {s}"
                    )

            else:

                st.markdown(
                    "None — all standard sections detected."
                )

        st.markdown(
            "### 🛠️ Skills Detected"
        )

        for category, skills in (
            result[
                "resume_skills_by_cat"
            ].items()
        ):

            st.markdown(
                f"**{category}:** "
                f"{', '.join(skills)}"
            )

        st.markdown(
            "### 💡 Resume Improvement Recommendations"
        )

        if result["suggestions"]:

            for suggestion in result[
                "suggestions"
            ]:

                st.markdown(
                    f"- {suggestion}"
                )

        else:

            st.info(
                "No additional recommendations."
            )

        if st.session_state.user:

            if st.button(
                "💾 Save this Analysis"
            ):

                jm = result.get(
                    "job_match_result"
                )

                db.save_analysis(
                    user_id=st.session_state.user[
                        "id"
                    ],

                    resume_filename=result.get(
                        "filename",
                        "resume"
                    ),

                    ats_score=result[
                        "ats_result"
                    ][
                        "total_score"
                    ],

                    job_match_score=(
                        jm[
                            "job_match_percentage"
                        ]
                        if jm
                        else None
                    ),

                    result_dict={
                        "note":
                        "Full detail available in report."
                    },

                    matched_skills=(
                        jm[
                            "matched_skills"
                        ]
                        if jm
                        else []
                    ),

                    missing_skills=(
                        jm[
                            "missing_skills"
                        ]
                        if jm
                        else []
                    ),
                )

                st.success(
                    "Analysis saved to your history."
                )


# ============================================================
# ATS SCORE
# ============================================================

def page_ats_score():

    st.markdown(
        "## Estimated ATS Compatibility Score"
    )

    st.caption(
        "This is an estimated compatibility score based "
        "on this project's own scoring methodology — not "
        "an official score from any commercial ATS vendor."
    )

    st.markdown("---")

    result = (
        st.session_state.current_analysis
    )

    if not result:

        st.info(
            "Run an analysis on the Resume Analyzer page first."
        )

        return

    ats = result[
        "ats_result"
    ]

    st.markdown(
        f"""
        <div class="metric-card">
            <h2>{ats['total_score']} / 100</h2>
            <p>Rating: {ats['rating']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(
        min(
            ats["total_score"] / 100,
            1.0
        )
    )

    st.markdown(
        "### Score Breakdown"
    )

    for name, comp in ats[
        "components"
    ].items():

        st.markdown(
            f"**{name}: "
            f"{comp['score']} / "
            f"{comp['max']}**"
        )

        st.caption(
            comp["explanation"]
        )

        st.progress(
            min(
                comp["score"] /
                comp["max"],
                1.0
            )
        )

    st.markdown(
        "### Weak Areas"
    )

    quality_issues = ats[
        "components"
    ][
        "Text Quality"
    ][
        "issues"
    ]

    if quality_issues:

        for issue in quality_issues:

            st.markdown(
                f"- {issue}"
            )

    else:

        st.markdown(
            "No major text quality issues detected."
        )


# ============================================================
# JOB MATCHER
# ============================================================

def page_job_matcher():

    st.markdown(
        "## Job Matcher"
    )

    st.caption(
        "Compare your resume against a job description "
        "using TF-IDF similarity and skill matching."
    )

    st.markdown("---")

    result = (
        st.session_state.current_analysis
    )

    if not result:

        st.info(
            "Run an analysis on the Resume Analyzer page first."
        )

        return

    jm = result.get(
        "job_match_result"
    )

    if not jm:

        st.warning(
            "No job description was provided during analysis. "
            "Go back to Resume Analyzer, paste a job description, "
            "and re-run the analysis."
        )

        return

    st.markdown(
        f"""
        <div class="metric-card">
            <h2>{jm['job_match_percentage']}%</h2>
            <p>Job Match Percentage</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        f"Calculated from: "
        f"{jm['skill_match_ratio']}% skill overlap "
        f"(weighted 60%) + "
        f"{jm['text_similarity']}% TF-IDF text similarity "
        f"(weighted 40%)."
    )

    col1, col2 = st.columns(
        2
    )

    with col1:

        st.markdown(
            "### Matched Skills"
        )

        st.write(
            ", ".join(
                jm["matched_skills"]
            )
            or "None found"
        )

    with col2:

        st.markdown(
            "### Missing Skills"
        )

        st.write(
            ", ".join(
                jm["missing_skills"]
            )
            or "None — great coverage!"
        )


# ============================================================
# KEYWORD SUGGESTIONS
# ============================================================

def page_keyword_suggestions():

    st.markdown(
        "## Keyword Suggestions"
    )

    st.caption(
        "Keywords found in the job description but missing "
        "from your resume, grouped by category."
    )

    st.markdown("---")

    result = (
        st.session_state.current_analysis
    )

    if not result:

        st.info(
            "Run an analysis on the Resume Analyzer page first."
        )

        return

    kw = result[
        "keyword_result"
    ]

    if not kw["by_category"]:

        note = kw.get(
            "note",
            "No missing keywords found."
        )

        if "No job description" in note:

            st.info(
                "No job description was provided."
            )

        else:

            st.info(
                note
            )

        return

    st.warning(
        kw["note"]
    )

    for category, keywords in kw[
        "by_category"
    ].items():

        st.markdown(
            f"**{category}:** "
            f"{', '.join(keywords)}"
        )


# ============================================================
# SKILL GAP
# ============================================================

def page_skill_gap():

    st.markdown(
        "## Skill Gap Analysis"
    )

    st.caption(
        "Skills you already have vs. skills required by "
        "the job description, with learning priority."
    )

    st.markdown("---")

    result = (
        st.session_state.current_analysis
    )

    if not result:

        st.info(
            "Run an analysis on the Resume Analyzer page first."
        )

        return

    sg = result[
        "skill_gap_result"
    ]

    if (
        not sg.get("already_have")
        and not sg.get("missing")
    ):

        st.info(
            "No job description was provided, or no recognized "
            "skills were found in it."
        )

        return

    st.markdown(
        "### Already Have"
    )

    st.write(
        ", ".join(
            sg["already_have"]
        )
        or "None"
    )

    st.markdown(
        "### Missing / Skill Gap"
    )

    if sg["missing"]:

        df = pd.DataFrame(
            sg["missing"]
        )

        df.columns = [
            "Skill",
            "Mentions in JD",
            "Priority"
        ]

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.write(
            "No skill gaps identified."
        )

    st.caption(
        sg["note"]
    )


# ============================================================
# ANALYSIS REPORT
# ============================================================

def page_analysis_report():

    st.markdown(
        "## Analysis Report"
    )

    st.caption(
        "Full summary of the current analysis, "
        "with a downloadable PDF."
    )

    st.markdown("---")

    result = (
        st.session_state.current_analysis
    )

    if not result:

        st.info(
            "Run an analysis on the Resume Analyzer page first."
        )

        return

    ats = result[
        "ats_result"
    ]

    jm = result.get(
        "job_match_result"
    )

    st.markdown(
        f"**Estimated ATS Compatibility:** "
        f"{ats['total_score']} / 100 "
        f"({ats['rating']})"
    )

    if jm:

        st.markdown(
            f"**Job Match Percentage:** "
            f"{jm['job_match_percentage']}%"
        )

    st.markdown(
        f"**Sections Present:** "
        f"{len(get_present_sections(result['sections']))} / "
        f"{len(result['sections'])}"
    )

    pdf_bytes = generate_pdf_report(
        {
            "ats_result":
                ats,

            "job_match_result":
                jm,

            "sections":
                result["sections"],

            "suggestions":
                result["suggestions"],

            "skill_gap_result":
                result["skill_gap_result"],

            "keyword_result":
                result["keyword_result"],
        }
    )

    st.download_button(
        label="Download Analysis Report (PDF)",
        data=pdf_bytes,
        file_name="resume_analysis_report.pdf",
        mime="application/pdf",
    )


# ============================================================
# ANALYSIS HISTORY
# ============================================================

def page_analysis_history():

    st.markdown(
        "## Analysis History"
    )

    st.caption(
        "Your previously saved resume analyses."
    )

    st.markdown("---")

    user = st.session_state.user

    analyses = db.get_user_analyses(
        user["id"]
    )

    if not analyses:

        st.info(
            "No saved analyses yet."
        )

        return

    for a in analyses:

        with st.expander(
            f"{a['resume_filename']} — "
            f"ATS: {a['ats_score']} — "
            f"{a['created_at'][:16].replace('T', ' ')}"
        ):

            st.markdown(
                f"**ATS Score:** "
                f"{a['ats_score']} / 100"
            )

            if a[
                "job_match_score"
            ] is not None:

                st.markdown(
                    f"**Job Match:** "
                    f"{a['job_match_score']}%"
                )

            else:

                st.markdown(
                    "**Job Match:** N/A"
                )

            conn = db.get_connection()
            cur = conn.cursor()

            cur.execute(
                """
                SELECT skill, status
                FROM analysis_skills
                WHERE analysis_id = ?
                """,
                (a["id"],)
            )

            rows = cur.fetchall()

            conn.close()

            matched = [
                r["skill"]
                for r in rows
                if r["status"] == "matched"
            ]

            missing = [
                r["skill"]
                for r in rows
                if r["status"] == "missing"
            ]

            st.markdown(
                f"**Matched Skills:** "
                f"{', '.join(matched) or 'None'}"
            )

            st.markdown(
                f"**Missing Skills:** "
                f"{', '.join(missing) or 'None'}"
            )

    if st.button(
        "Clear All History",
        type="secondary"
    ):

        st.session_state[
            "confirm_clear"
        ] = True

    if st.session_state.get(
        "confirm_clear"
    ):

        st.warning(
            "This will permanently delete all your saved analyses."
        )

        c1, c2 = st.columns(
            2
        )

        if c1.button(
            "Yes, delete everything"
        ):

            db.clear_user_history(
                user["id"]
            )

            st.session_state[
                "confirm_clear"
            ] = False

            st.success(
                "History cleared."
            )

            st.rerun()

        if c2.button(
            "Cancel"
        ):

            st.session_state[
                "confirm_clear"
            ] = False

            st.rerun()


# ============================================================
# PROFILE
# ============================================================

def page_profile():

    st.markdown(
        "## Profile"
    )

    st.markdown("---")

    user = st.session_state.user

    profile = (
        db.get_profile(
            user["id"]
        )
        or {}
    )

    with st.form(
        "profile_form"
    ):

        col1, col2 = st.columns(
            2
        )

        with col1:

            name = st.text_input(
                "Name",
                value=user["name"]
            )

            education = st.text_input(
                "Education",
                value=profile.get(
                    "education"
                ) or ""
            )

            branch = st.text_input(
                "Branch",
                value=profile.get(
                    "branch"
                ) or ""
            )

        with col2:

            email = st.text_input(
                "Email",
                value=user["email"]
            )

            graduation_year = st.text_input(
                "Graduation Year",
                value=profile.get(
                    "graduation_year"
                ) or ""
            )

            target_role = st.text_input(
                "Target Job Role",
                value=profile.get(
                    "target_role"
                ) or ""
            )

        preferred_domain = st.text_input(
            "Preferred Technology/Domain",
            value=profile.get(
                "preferred_domain"
            ) or ""
        )

        submitted = st.form_submit_button(
            "Save Profile"
        )

        if submitted:

            if not auth.is_valid_email(
                email
            ):

                st.error(
                    "Please enter a valid email address."
                )

            else:

                db.update_user_basic(
                    user["id"],
                    name,
                    email
                )

                db.update_profile(
                    user["id"],
                    education,
                    branch,
                    graduation_year,
                    target_role,
                    preferred_domain
                )

                st.session_state.user = (
                    db.get_user_by_id(
                        user["id"]
                    )
                )

                st.success(
                    "Profile updated."
                )

                st.rerun()


# ============================================================
# SETTINGS
# ============================================================

def page_settings():

    st.markdown(
        "## Settings"
    )

    st.markdown("---")

    user = st.session_state.user

    settings = (
        db.get_settings(
            user["id"]
        )
        or {}
    )

    st.markdown(
        "### Account Settings"
    )

    with st.form(
        "account_settings_form"
    ):

        new_password = st.text_input(
            "New Password "
            "(leave blank to keep current)",
            type="password"
        )

        confirm_new_password = st.text_input(
            "Confirm New Password",
            type="password"
        )

        submitted = st.form_submit_button(
            "Update Password"
        )

        if submitted:

            if new_password:

                valid, msg = (
                    auth.is_valid_password(
                        new_password
                    )
                )

                if not valid:

                    st.error(
                        msg
                    )

                elif (
                    new_password
                    != confirm_new_password
                ):

                    st.error(
                        "Passwords do not match."
                    )

                else:

                    db.update_user_password(
                        user["id"],
                        auth.hash_password(
                            new_password
                        )
                    )

                    st.success(
                        "Password updated."
                    )

            else:

                st.info(
                    "No changes made."
                )

    st.markdown(
        "### Resume Analysis Settings"
    )

    with st.form(
        "analysis_settings_form"
    ):

        target_job_role = st.text_input(
            "Target Job Role",
            value=settings.get(
                "target_job_role"
            ) or ""
        )

        preferred_industry = st.text_input(
            "Preferred Industry",
            value=settings.get(
                "preferred_industry"
            ) or ""
        )

        matching_strictness = st.selectbox(
            "Skill Matching Strictness",
            [
                "Low",
                "Medium",
                "High"
            ],
            index=[
                "Low",
                "Medium",
                "High"
            ].index(
                settings.get(
                    "matching_strictness"
                )
                or "Medium"
            ),
        )

        min_keyword_relevance = st.slider(
            "Minimum Keyword Relevance Threshold (%)",
            0,
            100,
            value=int(
                settings.get(
                    "min_keyword_relevance"
                )
                or 50
            ),
        )

        submitted2 = st.form_submit_button(
            "Save Preferences"
        )

        if submitted2:

            db.update_settings(
                user["id"],
                target_job_role,
                preferred_industry,
                matching_strictness,
                min_keyword_relevance,
                settings.get(
                    "theme"
                )
                or "Light",
            )

            st.success(
                "Preferences saved."
            )

    st.markdown(
        "### Appearance"
    )

    theme = st.radio(
        "Theme",
        [
            "Light",
            "Dark"
        ],
        index=(
            0
            if (
                settings.get(
                    "theme"
                )
                or "Light"
            ) == "Light"
            else 1
        )
    )

    if theme == "Dark":

        st.caption(
            "Dark mode preference saved. "
            "(Default remains Light for this demo build.)"
        )

    if st.button(
        "Save Appearance"
    ):

        db.update_settings(
            user["id"],
            settings.get(
                "target_job_role"
            ),
            settings.get(
                "preferred_industry"
            ),
            settings.get(
                "matching_strictness"
            )
            or "Medium",
            settings.get(
                "min_keyword_relevance"
            )
            or 50,
            theme,
        )

        st.success(
            "Appearance preference saved."
        )

    st.markdown(
        "### Data Settings"
    )

    col1, col2 = st.columns(
        2
    )

    with col1:

        if st.button(
            "Clear Analysis History"
        ):

            st.session_state[
                "settings_confirm_clear"
            ] = True

    with col2:

        if st.button(
            "Delete Account",
            type="secondary"
        ):

            st.session_state[
                "settings_confirm_delete"
            ] = True

    if st.session_state.get(
        "settings_confirm_clear"
    ):

        st.warning(
            "This will permanently delete all your saved analyses."
        )

        c1, c2 = st.columns(
            2
        )

        if c1.button(
            "Confirm Clear History"
        ):

            db.clear_user_history(
                user["id"]
            )

            st.session_state[
                "settings_confirm_clear"
            ] = False

            st.success(
                "History cleared."
            )

        if c2.button(
            "Cancel Clear"
        ):

            st.session_state[
                "settings_confirm_clear"
            ] = False

    if st.session_state.get(
        "settings_confirm_delete"
    ):

        st.error(
            "This will permanently delete your account "
            "and all associated data. This cannot be undone."
        )

        c1, c2 = st.columns(
            2
        )

        if c1.button(
            "Confirm Delete Account"
        ):

            db.delete_user(
                user["id"]
            )

            st.session_state[
                "settings_confirm_delete"
            ] = False

            logout()

            st.success(
                "Account deleted."
            )

            st.rerun()

        if c2.button(
            "Cancel Delete"
        ):

            st.session_state[
                "settings_confirm_delete"
            ] = False


# ============================================================
# ABOUT
# ============================================================

def page_about():

    st.markdown(
        "## About Project"
    )

    st.markdown("---")

    st.markdown(
        "### AI Resume Analyzer & Job Matcher"
    )

    st.write(
        "A Python-based NLP and Machine Learning application "
        "designed to help students and job seekers analyze "
        "their resumes and compare their skills with job requirements."
    )

    st.markdown(
        "**Technology:** Python, NLP, Machine Learning, "
        "Streamlit, SQLite"
    )

    st.markdown(
        "### Main Capabilities"
    )

    st.markdown(
        """
- Resume content analysis
- Estimated ATS compatibility scoring
- Job description matching (TF-IDF + skill overlap)
- Keyword suggestions
- Skill gap identification with learning priority
- Resume improvement recommendations
- Personalized analysis history
"""
    )

    st.markdown(
        "### Limitations"
    )

    st.markdown(
        """
- The ATS score is an estimated compatibility score based on this project's own methodology, not an official score from any commercial ATS vendor.
- Different real-world ATS systems use different, proprietary algorithms.
- Skill extraction is limited to the local skills database and may not recognize every technology or niche tool.
- Formatting analysis (layout, fonts, images) is limited since analysis is based on extracted text.
- Results depend on the quality of text extraction from the uploaded file.
- The system does not and should not encourage users to add skills they do not genuinely have.
"""
    )

    st.caption(
        "Basic application-level security practices have been implemented "
        "(password hashing, session-based access control). Production "
        "deployment would require additional security hardening."
    )


# ============================================================
# MAIN ROUTING
# ============================================================

def main():

    if st.session_state.user is None:

        if (
            st.session_state.auth_page
            == "register"
        ):

            render_register_page()

        else:

            render_login_page()

        return

    user = st.session_state.user

    st.sidebar.markdown(
        f"### 👤 {user['name']}"
    )

    st.sidebar.caption(
        user["email"]
    )

    st.sidebar.markdown(
        "---"
    )

    pages = {

        "🏠 Dashboard":
            page_dashboard,

        "📄 Resume Analyzer":
            page_resume_analyzer,

        "🎯 ATS Score":
            page_ats_score,

        "💼 Job Matcher":
            page_job_matcher,

        "🔑 Keyword Suggestions":
            page_keyword_suggestions,

        "🧩 Skill Gap":
            page_skill_gap,

        "📊 Analysis Report":
            page_analysis_report,

        "🗂️ Analysis History":
            page_analysis_history,

        "👤 Profile":
            page_profile,

        "⚙️ Settings":
            page_settings,

        "ℹ️ About":
            page_about,
    }

    choice = st.sidebar.radio(
        "Navigation",
        list(pages.keys()),
        label_visibility="collapsed"
    )

    st.sidebar.markdown(
        "---"
    )

    if st.sidebar.button(
        "🚪 Logout"
    ):

        logout()
        st.rerun()

    pages[choice]()


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":
    main()