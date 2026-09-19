"""
title_comment_similarity.py
---------------------------
Takes a post title and a comment, embeds both with a sentence-transformer
model, and reports several similarity metrics.

Install:
    pip install sentence-transformers scikit-learn numpy
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import (
    cosine_similarity,
    euclidean_distances,
    manhattan_distances,
)


# ----------------------------------------------------------------------
# Model loading (cached after first run)
# ----------------------------------------------------------------------
DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
# Other good options:
#   "sentence-transformers/all-mpnet-base-v2"  (higher quality, slower)
#   "BAAI/bge-small-en-v1.5"                   (strong, small)
#   "intfloat/multilingual-e5-small"           (multilingual)


def load_model(name: str = DEFAULT_MODEL) -> SentenceTransformer:
    print(f"Loading embedding model: {name}")
    print("(First run downloads from HuggingFace; later runs use cache.)")
    return SentenceTransformer(name)


# ----------------------------------------------------------------------
# Similarity metrics
# ----------------------------------------------------------------------
def _safe_div(a: float, b: float) -> float:
    return a / b if b != 0 else 0.0


def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity in [-1, 1]; higher = more similar."""
    return float(cosine_similarity(a.reshape(1, -1), b.reshape(1, -1))[0, 0])


def euclidean_sim(a: np.ndarray, b: np.ndarray) -> float:
    """
    Convert Euclidean distance to a similarity in (0, 1] via 1 / (1 + d).
    Higher = more similar. Not scale-free like cosine, so mostly useful
    as a relative signal.
    """
    d = float(euclidean_distances(a.reshape(1, -1), b.reshape(1, -1))[0, 0])
    return 1.0 / (1.0 + d)


def manhattan_sim(a: np.ndarray, b: np.ndarray) -> float:
    """Manhattan (L1) distance → similarity via 1 / (1 + d)."""
    d = float(manhattan_distances(a.reshape(1, -1), b.reshape(1, -1))[0, 0])
    return 1.0 / (1.0 + d)


def dot_product(a: np.ndarray, b: np.ndarray) -> float:
    """Raw dot product. Only meaningful if vectors are normalized."""
    return float(np.dot(a, b))


def jaccard_word_sim(text_a: str, text_b: str) -> float:
    """Set-overlap of words (case-insensitive, punctuation stripped)."""
    tokens_a = set(re.findall(r"\w+", text_a.lower()))
    tokens_b = set(re.findall(r"\w+", text_b.lower()))
    if not tokens_a and not tokens_b:
        return 0.0
    return len(tokens_a & tokens_b) / len(tokens_a | tokens_b)


def jaccard_char_ngram_sim(text_a: str, text_b: str, n: int = 3) -> float:
    """Set-overlap of character n-grams. Robust to small spelling variants."""
    def grams(s: str):
        s = re.sub(r"\s+", " ", s.lower()).strip()
        return {s[i:i + n] for i in range(len(s) - n + 1)} if len(s) >= n else {s}

    ga, gb = grams(text_a), grams(text_b)
    if not ga and not gb:
        return 0.0
    return len(ga & gb) / len(ga | gb)


# ----------------------------------------------------------------------
# Full similarity report
# ----------------------------------------------------------------------
@dataclass
class SimilarityReport:
    title: str
    comment: str
    embedding_dim: int
    metrics: Dict[str, float]


def compute_similarities(
    title: str,
    comment: str,
    model: SentenceTransformer,
    normalize_embeddings: bool = True,
) -> SimilarityReport:
    # 1. Embed both texts (batched, single call is faster)
    embs = model.encode(
        [title, comment],
        normalize_embeddings=normalize_embeddings,
        convert_to_numpy=True,
    )
    emb_title, emb_comment = embs[0], embs[1]

    # 2. Compute metrics
    metrics = {
        "cosine_similarity":     cosine_sim(emb_title, emb_comment),
        "dot_product":           dot_product(emb_title, emb_comment),
        "euclidean_similarity":  euclidean_sim(emb_title, emb_comment),
        "manhattan_similarity":  manhattan_sim(emb_title, emb_comment),
        "jaccard_word":          jaccard_word_sim(title, comment),
        "jaccard_char_3gram":    jaccard_char_ngram_sim(title, comment, n=3),
        "length_ratio":          _safe_div(
            min(len(title), len(comment)), max(len(title), len(comment))
        ),
    }

    return SimilarityReport(
        title=title,
        comment=comment,
        embedding_dim=emb_title.shape[0],
        metrics=metrics,
    )


def format_report(r: SimilarityReport) -> str:
    lines = []
    lines.append("=" * 70)
    lines.append(f"TITLE   : {r.title}")
    lines.append(f"COMMENT : {r.comment}")
    lines.append(f"Embedding dim: {r.embedding_dim}")
    lines.append("-" * 70)

    # Group metrics for readability
    semantic = ["cosine_similarity", "dot_product",
                "euclidean_similarity", "manhattan_similarity"]
    lexical = ["jaccard_word", "jaccard_char_3gram", "length_ratio"]

    lines.append("Semantic (embedding-based):")
    for k in semantic:
        lines.append(f"  {k:<22} {r.metrics[k]:+.4f}")

    lines.append("Lexical (surface-level):")
    for k in lexical:
        lines.append(f"  {k:<22} {r.metrics[k]:+.4f}")

    # Quick interpretation
    cos = r.metrics["cosine_similarity"]
    if cos >= 0.75:
        verdict = "very similar (likely on-topic)"
    elif cos >= 0.5:
        verdict = "moderately similar (probably related)"
    elif cos >= 0.3:
        verdict = "loosely related"
    else:
        verdict = "weakly related or off-topic"
    lines.append("-" * 70)
    lines.append(f"Interpretation (cosine ≥ 0.75 → on-topic): {verdict}")
    lines.append("=" * 70)
    return "\n".join(lines)


# ----------------------------------------------------------------------
# Interactive CLI
# ----------------------------------------------------------------------
def main():
    model = load_model()

    print("\n" + "=" * 70)
    print("Title ↔ Comment Similarity")
    print("Enter a post title and a comment. Type 'quit' at either prompt to stop.")
    print("=" * 70)

    while True:
        try:
            title = input("\nPost title   > ").strip()
            if title.lower() in {"quit", "exit"}:
                print("Bye!")
                break
            if not title:
                print("(empty title — try again)")
                continue

            comment = input("Comment      > ").strip()
            if comment.lower() in {"quit", "exit"}:
                print("Bye!")
                break
            if not comment:
                print("(empty comment — try again)")
                continue
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        report = compute_similarities(title, comment, model)
        print()
        print(format_report(report))


if __name__ == "__main__":
    main()