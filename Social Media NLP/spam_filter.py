"""
spam_classifier_cli.py
----------------------
Interactive CLI version of the spam/ham classifier.

Downloads the TF-IDF vectorizer and Multinomial Naive Bayes model
from Google Drive (via gdown) on first run, then classifies whatever
text you type.

Requires env vars:
    VECTORIZER_ID   — Google Drive file ID for vectorizer.pkl
    MODEL_ID        — Google Drive file ID for spam_classifier.pkl

Install:
    pip install nltk gdown

Run:
    export VECTORIZER_ID="..."   # Linux/macOS
    export MODEL_ID="..."
    python spam_classifier_cli.py
"""

import os
import pickle
import string

import gdown
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from dotenv import load_dotenv
load_dotenv()   # reads .env and injects its vars into os.environ

# ----------------------------------------------------------------------
# NLTK resources (downloaded once, cached in ~/nltk_data)
# ----------------------------------------------------------------------
for pkg in ("punkt", "punkt_tab", "stopwords"):
    try:
        nltk.data.find(f"tokenizers/{pkg}" if "punkt" in pkg else f"corpora/{pkg}")
    except LookupError:
        nltk.download(pkg, quiet=True)

ps = PorterStemmer()
STOPWORDS = set(stopwords.words("english"))


# ----------------------------------------------------------------------
# Download model artifacts if not present
# ----------------------------------------------------------------------
def _ensure_file(path: str, env_var: str, friendly_name: str) -> None:
    if os.path.exists(path):
        return
    file_id = os.getenv(env_var)
    if not file_id:
        raise RuntimeError(
            f"Missing environment variable {env_var}. "
            f"Set it to the Google Drive file ID for {friendly_name}."
        )
    url = f"https://drive.google.com/uc?id={file_id}"
    print(f"Downloading {friendly_name} → {path} ...")
    gdown.download(url, path, quiet=False)


_ensure_file("vectorizer.pkl", "VECTORIZER_ID", "vectorizer.pkl")
_ensure_file("spam_classifier.pkl", "MODEL_ID", "spam_classifier.pkl")

print("Loading model artifacts...")
with open("vectorizer.pkl", "rb") as f:
    tfidf = pickle.load(f)
with open("spam_classifier.pkl", "rb") as f:
    mnb = pickle.load(f)


# ----------------------------------------------------------------------
# Preprocessing (identical to the Streamlit version)
# ----------------------------------------------------------------------
def transform_text(text: str) -> str:
    text = text.lower()
    tokens = nltk.word_tokenize(text)

    # 1. Keep alphanumeric only
    tokens = [t for t in tokens if t.isalnum()]

    # 2. Drop stopwords and punctuation
    tokens = [t for t in tokens if t not in STOPWORDS and t not in string.punctuation]

    # 3. Stem
    tokens = [ps.stem(t) for t in tokens]

    return " ".join(tokens)


def classify(text: str) -> tuple[int, str]:
    """Return (label_int, label_str). label_int: 0 = ham, 1 = spam."""
    transformed = transform_text(text)
    vector = tfidf.transform([transformed])
    pred = int(mnb.predict(vector)[0])
    return pred, ("Spam" if pred == 1 else "Not spam")


# ----------------------------------------------------------------------
# Interactive CLI
# ----------------------------------------------------------------------
def main() -> None:
    print("=" * 70)
    print("Spam or Ham — SMS classifier")
    print("Type a message and press Enter. 'quit' or 'exit' to stop.")
    print("=" * 70)

    while True:
        try:
            user_input = input("\nMessage > ").strip()
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