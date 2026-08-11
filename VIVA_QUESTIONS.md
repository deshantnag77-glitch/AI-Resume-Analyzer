# Viva Questions and Answers

**Q1. What is the objective of this project?**
To help students and job seekers analyze their resumes, estimate ATS compatibility, and
compare their skills against a specific job description, so they can identify and fix gaps
before applying.

**Q2. Why did you use TF-IDF instead of a deep learning model like BERT?**
TF-IDF + cosine similarity is a well-established, explainable, lightweight NLP technique
that runs fully offline without downloading large pretrained models. For a resume-matching
use case at this scale, it gives meaningful, interpretable results while keeping the
project simple enough to explain component-by-component during evaluation. BERT-based
semantic similarity is listed as a future improvement.

**Q3. How is the ATS score calculated?**
It is a weighted sum of four components, each scored out of 25: Structure & Section
Completeness, Skills Relevance, Text Quality, and Job Description Match. Each component
has its own explainable calculation (e.g., Structure is the fraction of standard resume
sections detected).

**Q4. Is your ATS score the same as a real company's ATS score?**
No. It is clearly labeled "Estimated ATS Compatibility Score," calculated using this
project's own transparent methodology. Real commercial ATS systems use different,
proprietary algorithms that are not publicly disclosed.

**Q5. How is the Job Match Percentage calculated?**
Job Match % = (0.6 × Skill Overlap %) + (0.4 × TF-IDF Cosine Similarity %). Skill Overlap
is the fraction of job-description skills also found in the resume; TF-IDF similarity
measures overall textual relevance between the two documents.

**Q6. How do you extract skills from the resume and job description?**
Using a local CSV-based skills database (`data/skills.csv`) covering categories like
Programming Languages, Data Science, ML, Web Development, Databases, Cloud, DevOps, Tools,
and Soft Skills. Each skill is matched using word-boundary regex so partial-word false
matches (e.g., "R" inside "Random") are avoided.

**Q7. How do you detect resume sections?**
Using regex-based keyword/heading matching — for example, looking for terms like
"education," "b.tech," "cgpa" to detect an Education section, or "projects,"
"academic projects" for a Projects section.

**Q8. How is skill gap priority decided?**
By counting how many times each missing skill is mentioned in the job description text —
more mentions suggest higher importance to the role, so it's labeled High Priority (3+
mentions), Medium (2), or Low (1).

**Q9. How do you handle invalid or empty resumes?**
The resume parser raises a custom `ResumeParseError` with a friendly message for cases
like unsupported file types, empty files, PDFs with no extractable text (e.g., scanned
images), and resumes that are too short to analyze meaningfully.

**Q10. How are user passwords stored?**
Passwords are never stored in plain text. They are hashed using bcrypt before being saved
to the SQLite database, and login compares the entered password's hash against the stored
hash.

**Q11. How do you ensure one user can't see another user's analysis history?**
All database queries for analyses and profile data are scoped by `user_id`, and the
`get_analysis_by_id` function explicitly checks that the requesting user_id matches the
analysis owner before returning any data.

**Q12. Why did you choose SQLite instead of MySQL/PostgreSQL?**
SQLite is a lightweight, file-based database that requires no separate server setup,
making it well suited for a college demonstration project while still supporting proper
relational structure (foreign keys, multiple related tables).

**Q13. Does the score change for different resumes, or is it hardcoded?**
It changes based on actual content. Testing with a detailed, well-structured resume versus
a short, generic one produced clearly different scores (~65-70/100 vs. ~18/100), confirming
the analysis is genuinely computed, not static or random.

**Q14. What happens if no job description is provided?**
The Job Description Match component of the ATS score falls back to a conservative
estimate based on general skill breadth alone, and the UI clearly indicates that pasting a
job description will produce a more accurate score. Job Matcher, Keyword Suggestions, and
Skill Gap pages show an informational message if no JD was provided.

**Q15. What are the main limitations of this project?**
The ATS score is an estimate, not an official score from any real ATS vendor; skill
recognition is limited to the local database; formatting/layout analysis is limited since
it works on extracted text; and results depend on how well text was extracted from the
uploaded file.

**Q16. What security measures have you implemented?**
Password hashing (bcrypt), session-based authentication, user-scoped data access,
confirmation prompts before destructive actions (clearing history, deleting account), and
input validation on registration/login forms. The report explicitly notes that production
deployment would need additional hardening.

**Q17. Can this project be extended in the future?**
Yes — planned future improvements include transformer-based (BERT) semantic similarity,
automated resume section classification via a trained ML model, job portal integration,
multi-language resume support, and cloud deployment.

**Q18. Why does the tool warn users not to add skills they don't have?**
To keep the tool ethically sound and genuinely useful — recommending users artificially
insert keywords they have no real experience with would misrepresent their qualifications
and could backfire in an interview. The tool's keyword suggestions explicitly include this
caution.
