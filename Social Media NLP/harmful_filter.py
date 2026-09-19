"""
content_filter_cli.py
---------------------
Interactive CLI version of the inappropriate-content filter.

Downloads the TF-IDF vectorizer and Multinomial Naive Bayes model
from Google Drive (via gdown) on first run, then classifies whatever
text you type.

Install:
    pip install nltk gdown python-dotenv

.env (in the same folder as this script):
    VECTORIZER_ID=...
    MODEL_ID=...

Run:
    python content_filter_cli.py
"""

import os
import pickle
import string

import gdown
import nltk
from dotenv import load_dotenv
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


# ----------------------------------------------------------------------
# Load env vars from .env (must happen BEFORE os.getenv calls)
# ----------------------------------------------------------------------
load_dotenv()

VECTORIZER_ID = os.getenv("VECTORIZER_ID")
MODEL_ID      = os.getenv("MODEL_ID")


# ----------------------------------------------------------------------
# NLTK resources (downloaded once, cached in ~/nltk_data)
# ----------------------------------------------------------------------
for pkg in ("punkt", "punkt_tab", "stopwords"):
    subdir = "tokenizers" if "punkt" in pkg else "corpora"
    try:
        nltk.data.find(f"{subdir}/{pkg}")
    except LookupError:
        nltk.download(pkg, quiet=True)

ps = PorterStemmer()
STOPWORDS = set(stopwords.words("english"))


# ----------------------------------------------------------------------
# Download model artifacts if not present
# ----------------------------------------------------------------------
def _ensure_file(path: str, file_id: str | None, friendly_name: str) -> None:
    if os.path.exists(path):
        return
    if not file_id:
        raise RuntimeError(
            f"Missing file ID for {friendly_name}. "
            f"Set VECTORIZER_ID / MODEL_ID in your .env file."
        )
    url = f"https://drive.google.com/uc?id={file_id}"
    print(f"Downloading {friendly_name} → {path} ...")
    gdown.download(url, path, quiet=False)


_ensure_file("content_vectorizer.pkl", VECTORIZER_ID, "content_vectorizer.pkl")
_ensure_file("content_classifier.pkl", MODEL_ID, "content_classifier.pkl")

print("Loading model artifacts...")
with open("content_vectorizer.pkl", "rb") as f:
    tfidf = pickle.load(f)
with open("content_classifier.pkl", "rb") as f:
    mnb = pickle.load(f)


# ----------------------------------------------------------------------
# Preprocessing (identical to the Streamlit version)
# ----------------------------------------------------------------------
def transform_text(text: str) -> str:
    text = text.lower()

    # 1. Drop @mentions and retweet prefix tokens
    tokens = [t for t in text.split() if t and t[0] != "@" and t != "rt"]
    text = " ".join(tokens)

    # 2. Tokenize
    tokens = nltk.word_tokenize(text)

    # 3. Keep only alphabetic tokens (removes punctuation, numbers, etc.)
    tokens = [t for t in tokens if t.isalpha()]

    # 4. Drop stopwords and punctuation
    tokens = [t for t in tokens if t not in STOPWORDS and t not in string.punctuation]

    # 5. Stem
    tokens = [ps.stem(t) for t in tokens]

    return " ".join(tokens)


def classify(text: str) -> tuple[int, str]:
    """
    Return (label_int, label_str).
    label_int: 0 = appropriate, 1 = inappropriate.
    """
    transformed = transform_text(text)
    vector = tfidf.transform([transformed])
    pred = int(mnb.predict(vector)[0])
    return pred, ("Inappropriate content" if pred == 1 else "Appropriate content")


# ----------------------------------------------------------------------
# Interactive CLI
# ----------------------------------------------------------------------
def main() -> None:
    print("=" * 70)
    print("Inappropriate Content Filter")
    print("Type a message and press Enter. 'quit' or 'exit' to stop.")
    print("=" * 70)

    while True:
        try:
            user_input = input("\nText > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not user_input:
            continue
        if user_input.lower() in {"quit", "exit"}:
            print("Bye!")
            break

        try:
            pred, label = classify(user_input)
            print(f"Prediction : {label}  (class={pred})")
        except Exception as e:
            print(f"[Error] {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()