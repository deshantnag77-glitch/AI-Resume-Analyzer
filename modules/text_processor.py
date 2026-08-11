"""
text_processor.py
------------------
Basic NLP text cleaning utilities used across the pipeline.
Deliberately lightweight (regex + simple tokenization) so the project
can run fully offline without large model downloads.
"""

import re
from collections import Counter

# A small, practical stopword list (avoids needing an NLTK data download
# for a college demo environment).
STOPWORDS = set("""
a an the and or but if while is are was were be been being have has had
do does did will would shall should can could may might must to of in
on at by for with about against between into through during before after
above below from up down out off over under again further then once here
there when where why how all any both each few more most other some such
no nor not only own same so than too very s t just don now i me my myself
we our ours ourselves you your yours yourself yourselves he him his himself
she her hers herself it its itself they them their theirs themselves what
which who whom this that these those am as
""".split())

GENERIC_PHRASES = [
    "hard working", "hardworking", "team player", "fast learner",
    "detail oriented", "self motivated", "go getter", "results driven",
    "highly motivated", "passionate about", "think outside the box",
    "dynamic individual", "excellent communication skills",
]


def clean_text(text: str) -> str:
    """Lowercase, remove extra whitespace and non-informative characters."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s\+\#\.\-/]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text: str) -> list:
    """Simple word tokenizer with stopword removal."""
    cleaned = clean_text(text)
    tokens = cleaned.split()
    return [t for t in tokens if t not in STOPWORDS and len(t) > 1]


def get_word_frequency(text: str, top_n: int = 15) -> list:
    """Return the most frequent meaningful words (for repetition analysis)."""
    tokens = tokenize(text)
    counts = Counter(tokens)
    return counts.most_common(top_n)


def detect_repeated_words(text: str, threshold: int = 6) -> list:
    """Flag words that appear unusually often (possible overuse)."""
    freq = get_word_frequency(text, top_n=30)
    return [(word, count) for word, count in freq if count >= threshold]


def detect_generic_phrases(text: str) -> list:
    """Find generic/cliche phrases that add little value to a resume."""
    lowered = text.lower()
    found = [phrase for phrase in GENERIC_PHRASES if phrase in lowered]
    return found


def has_measurable_achievements(text: str) -> bool:
    """
    Heuristic check for quantifiable achievements:
    numbers followed by %, or standalone numbers near achievement verbs.
    """
    if re.search(r"\d+\s?%", text):
        return True
    if re.search(r"\b(increased|reduced|improved|achieved|generated|saved|grew|built|led)\b.{0,40}\d+", text, re.IGNORECASE):
        return True
    return False


def word_count(text: str) -> int:
    return len(text.split())


def sentence_count(text: str) -> int:
    sentences = re.split(r"[.!?]\s+", text)
    return len([s for s in sentences if s.strip()])
