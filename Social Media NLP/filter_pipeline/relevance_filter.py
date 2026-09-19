"""
relevance_filter.py
-------------------
Title ↔ Comment relevance check using sentence embeddings + multiple
distance metrics. A comment is RELEVANT if ANY metric >= threshold.

Install:
    pip install sentence-transformers scikit-learn numpy
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import (
    cosine_similarity,
    euclidean_distances,
    manhattan_distances,
)


DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


# ----------------------------------------------------------------------
# Metric helpers
# ----------------------------------------------------------------------
def _safe_div(a: float, b: float) -> float:
    return a / b if b != 0 else 0.0


def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    return float(cosine_similarity(a.reshape(1, -1), b.reshape(1, -1))[0, 0])


def euclidean_sim(a: np.ndarray, b: np.ndarray) -> float:
    d = float(euclidean_distances(a.reshape(1, -1), b.reshape(1, -1))[0, 0])
    return 1.0 / (1.0 + d)


def manhattan_sim(a: np.ndarray, b: np.ndarray) -> float:
    d = float(manhattan_distances(a.reshape(1, -1), b.reshape(1, -1))[0, 0])
    return 1.0 / (1.0 + d)


def dot_product(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b))


def jaccard_word_sim(text_a: str, text_b: str) -> float:
    ta = set(re.findall(r"\w+", text_a.lower()))
    tb = set(re.findall(r"\w+", text_b.lower()))
    if not ta and not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def jaccard_char_ngram_sim(text_a: str, text_b: str, n: int = 3) -> float:
    def grams(s: str):
        s = re.sub(r"\s+", " ", s.lower()).strip()
        return {s[i:i + n] for i in range(len(s) - n + 1)} if len(s) >= n else {s}
    ga, gb = grams(text_a), grams(text_b)
    if not ga and not gb:
        return 0.0
    return len(ga & gb) / len(ga | gb)


# ----------------------------------------------------------------------
# Result containers
# ----------------------------------------------------------------------
@dataclass
class SimilarityReport:
    title: str
    comment: str
    embedding_dim: int
    metrics: Dict[str, float] = field(default_factory=dict)


@dataclass
class RelevanceResult:
    is_relevant: bool
    threshold: float
    passed_metrics: List[str] = field(default_factory=list)
    metrics: Dict[str, float] = field(default_factory=dict)
    report: Optional[SimilarityReport] = None


# ----------------------------------------------------------------------
# Filter
# ----------------------------------------------------------------------
class RelevanceFilter:
    """Compute multiple similarity metrics; relevant if any >= threshold."""

    CANDIDATE_METRICS = [
        "cosine_similarity",
        "euclidean_similarity",
        "manhattan_similarity",
        "jaccard_word",
        "jaccard_char_3gram",
        "length_ratio",
    ]

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
        threshold: float = 0.15,
        normalize_embeddings: bool = True,
    ):
        self.model_name = model_name
        self.threshold = threshold
        self.normalize_embeddings = normalize_embeddings
        self._model: Optional[SentenceTransformer] = None

    def _load(self):
        if self._model is None:
            print(f"Loading embedding model: {self.model_name}")
            print("(First run downloads from HuggingFace; later runs use cache.)")
            self._model = SentenceTransformer(self.model_name)

    def evaluate(self, title: str, comment: str) -> RelevanceResult:
        """Never raises — returns safe default on failure."""
        if not title or not title.strip() or not comment or not comment.strip():
            return RelevanceResult(
                is_relevant=False,
                threshold=self.threshold,
                passed_metrics=[],
                metrics={},
            )

        try:
            self._load()
            embs = self._model.encode(
                [title, comment],
                normalize_embeddings=self.normalize_embeddings,
                convert_to_numpy=True,
            )
            emb_t, emb_c = embs[0], embs[1]
        except Exception as e:
            print(f"[relevance_filter] Embedding failed: {type(e).__name__}: {e}")
            return RelevanceResult(
                is_relevant=False,
                threshold=self.threshold,
                passed_metrics=[],
                metrics={},
            )

        metrics: Dict[str, float] = {
            "cosine_similarity":    cosine_sim(emb_t, emb_c),
            "dot_product":          dot_product(emb_t, emb_c),
            "euclidean_similarity": euclidean_sim(emb_t, emb_c),
            "manhattan_similarity": manhattan_sim(emb_t, emb_c),
            "jaccard_word":         jaccard_word_sim(title, comment),
            "jaccard_char_3gram":   jaccard_char_ngram_sim(title, comment, n=3),
            "length_ratio":         _safe_div(
                min(len(title), len(comment)), max(len(title), len(comment))
            ),
        }

        passed = [
            name for name in self.CANDIDATE_METRICS
            if metrics[name] >= self.threshold
        ]

        report = SimilarityReport(
            title=title,
            comment=comment,
            embedding_dim=int(emb_t.shape[0]),
            metrics=metrics,
        )

        return RelevanceResult(
            is_relevant=len(passed) > 0,
            threshold=self.threshold,
            passed_metrics=passed,
            metrics=metrics,
            report=report,
        )