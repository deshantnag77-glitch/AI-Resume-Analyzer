# Testing Instructions

## 1. Setup

```bash
cd AI_Resume_Analyzer
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

The app opens at `http://localhost:8501`. A SQLite database is created automatically at
`database/resume_analyzer.db` on first run.

## 2. Test Account Flow

1. Click **Create an Account** on the login page.
2. Register with:
   - Name: `Test Student`
   - Email: `test@example.com`
   - Password: `Test1234` (must be 8+ chars, at least one letter and one number)
3. Log in with the same credentials.
4. Confirm you land on the **Dashboard** with all metrics at 0 (no analyses yet).

## 3. Test Resume Analysis (Core Pipeline)

1. Go to **Resume Analyzer**.
2. Upload `assets/sample_resume.txt` (included in this repo).
3. Paste the contents of `assets/sample_job_description.txt` into the Job Description box.
4. Click **Analyze Resume**.
5. Verify:
   - Extracted text preview appears and is readable.
   - Detected sections list shows most sections present, "Experience" missing (this is a
     known property of the sample resume — it uses an "Internships" heading instead).
   - Skills Detected shows categorized skills (Python, SQL, Pandas, etc.).
   - Resume Improvement Recommendations lists specific, non-generic suggestions.
6. Click **Save this Analysis** and confirm a success message appears.

## 4. Test Each Analysis Page

With the analysis above still active in session:

- **ATS Score:** Confirm a total score (0-100), a rating label, and a 4-component
  breakdown with progress bars and explanations.
- **Job Matcher:** Confirm a Job Match Percentage, matched skills, and missing skills.
- **Keyword Suggestions:** Confirm missing keywords grouped by category (e.g., Cloud
  Technologies: AWS) with the "only add skills you genuinely know" caution shown.
- **Skill Gap:** Confirm a table of missing skills with mention counts and priority labels.
- **Analysis Report:** Click **Download Analysis Report (PDF)** and confirm a PDF
  downloads and opens correctly with all sections populated.

## 5. Test Analysis History

1. Go to **Analysis History**.
2. Confirm the saved analysis from Step 3 appears with correct ATS score and date.
3. Expand it and confirm matched/missing skills are listed.
4. Test **Clear All History** and confirm the confirmation prompt appears before deletion.

## 6. Test Profile & Settings

1. Go to **Profile**, fill in Education/Branch/Graduation Year/Target Role, save, and
   confirm the values persist after a page refresh.
2. Go to **Settings**:
   - Update password and confirm you can log in with the new password after logging out.
   - Change Skill Matching Strictness and Minimum Keyword Relevance, save, and confirm no
     errors.
   - Test **Delete Account** and confirm a confirmation prompt appears before the account
     (and all its analyses) is deleted.

## 7. Test Error Handling

- Upload a `.jpg` file — should show "Unsupported file format."
- Upload an empty `.txt` file — should show an empty/too-short file error.
- Try analyzing without uploading a file — should show "Please upload a resume file first."
- Try registering with mismatched passwords — should show "Passwords do not match."
- Try registering with an already-used email — should show a duplicate-account error.
- Try logging in with a wrong password — should show "Incorrect password."

## 8. Test Non-Randomness (Important for VT Evaluation)

Run the analysis twice with the exact same resume and job description. Confirm the ATS
score and job match percentage are **identical** both times (deterministic, not random).

Then run it with two different resumes (e.g., a strong, detailed resume vs. a short,
generic one). Confirm the scores are meaningfully different and correctly reflect the
quality difference.
