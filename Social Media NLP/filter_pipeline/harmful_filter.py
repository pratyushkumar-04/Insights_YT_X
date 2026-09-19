"""
harmful_filter.py
-----------------
Inappropriate/harmful content filter (TF-IDF + Multinomial Naive Bayes).

Downloads content_vectorizer.pkl and content_classifier.pkl from
Google Drive via gdown on first run.

Requires env vars (distinct from spam_filter to avoid collisions):
    HARM_VECTORIZER_ID   — Google Drive file ID for content_vectorizer.pkl
    HARM_MODEL_ID        — Google Drive file ID for content_classifier.pkl

Install:
    pip install nltk gdown python-dotenv
"""

from __future__ import annotations

import os
import pickle
import string
from dataclasses import dataclass
from typing import Optional

import gdown
import nltk
from dotenv import load_dotenv
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

load_dotenv()


# ----------------------------------------------------------------------
# NLTK resources
# ----------------------------------------------------------------------
for pkg in ("punkt", "punkt_tab", "stopwords"):
    subdir = "tokenizers" if "punkt" in pkg else "corpora"
    try:
        nltk.data.find(f"{subdir}/{pkg}")
    except LookupError:
        nltk.download(pkg, quiet=True)

_ps = PorterStemmer()
_STOPWORDS = set(stopwords.words("english"))


# ----------------------------------------------------------------------
# Model paths + download
# ----------------------------------------------------------------------
VECTORIZER_PATH = "content_vectorizer.pkl"
CLASSIFIER_PATH = "content_classifier.pkl"


def _ensure_file(path: str, env_var: str, friendly_name: str) -> None:
    if os.path.exists(path):
        return
    file_id = os.getenv(env_var)
    if not file_id:
        raise RuntimeError(
            f"Missing environment variable {env_var}. "
            f"Set it in your .env to the Google Drive file ID for {friendly_name}."
        )
    url = f"https://drive.google.com/uc?id={file_id}"
    print(f"Downloading {friendly_name} → {path} ...")
    gdown.download(url, path, quiet=False)


# ----------------------------------------------------------------------
# Preprocessing
# ----------------------------------------------------------------------
def transform_text(text: str) -> str:
    text = text.lower()

    # Drop @mentions and "rt" prefix tokens
    tokens = [t for t in text.split() if t and t[0] != "@" and t != "rt"]
    text = " ".join(tokens)

    tokens = nltk.word_tokenize(text)
    tokens = [t for t in tokens if t.isalpha()]
    tokens = [t for t in tokens if t not in _STOPWORDS and t not in string.punctuation]
    tokens = [_ps.stem(t) for t in tokens]

    return " ".join(tokens)


# ----------------------------------------------------------------------
# Result + filter
# ----------------------------------------------------------------------
@dataclass
class HarmfulResult:
    is_harmful: bool
    label: str
    class_int: int
    transformed_text: str


class HarmfulFilter:
    def __init__(self):
        self._tfidf = None
        self._mnb = None

    def _load(self):
        if self._tfidf is None or self._mnb is None:
            _ensure_file(VECTORIZER_PATH, "HARM_VECTORIZER_ID", "content_vectorizer.pkl")
            _ensure_file(CLASSIFIER_PATH, "HARM_MODEL_ID", "content_classifier.pkl")
            print("Loading harmful-content model artifacts...")
            with open(VECTORIZER_PATH, "rb") as f:
                self._tfidf = pickle.load(f)
            with open(CLASSIFIER_PATH, "rb") as f:
                self._mnb = pickle.load(f)

    def classify(self, text: str) -> HarmfulResult:
        """Never raises — safe default on failure."""
        if not isinstance(text, str) or not text.strip():
            return HarmfulResult(False, "Appropriate content", 0, "")
        try:
            self._load()
            transformed = transform_text(text)
            vector = self._tfidf.transform([transformed])
            pred = int(self._mnb.predict(vector)[0])
            label = "Inappropriate content" if pred == 1 else "Appropriate content"
            return HarmfulResult(pred == 1, label, pred, transformed)
        except Exception as e:
            print(f"[harmful_filter] Error: {type(e).__name__}: {e}")
            return HarmfulResult(False, "Appropriate content", 0, "")