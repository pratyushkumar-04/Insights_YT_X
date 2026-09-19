"""
language_detection.py
---------------------
Language detection using linguonnx (glotlid-int8).

First call downloads ~419 MB model to ~/.cache/linguonnx/models/.
"""

from __future__ import annotations

import logging
from typing import List, Optional, Tuple

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------
# Language code aliases (ISO 639-2 → 639-1 for Indic languages)
# ----------------------------------------------------------------------
LANG_ALIASES = {
    "ory": "or", "ori": "or", "pan": "pa", "san": "sa", "snd": "sd",
    "sin": "si", "tam": "ta", "tel": "te", "urd": "ur", "mal": "ml",
    "kan": "kn", "guj": "gu", "mar": "mr", "nep": "ne", "ben": "bn",
    "asm": "as", "hin": "hi",
}


def normalize_lang_code(code: str) -> str:
    """Normalize language code (strips region/script, maps aliases)."""
    base = code.split("-")[0].split("_")[0].lower()
    return LANG_ALIASES.get(base, base)


# ----------------------------------------------------------------------
# Detector wrapper
# ----------------------------------------------------------------------
class LanguageDetector:
    """
    Lazy-loading wrapper around linguonnx's glotlid detector.
    Thread-safe for read-only detect calls after load.
    """

    def __init__(self):
        self._det = None

    def _load(self):
        if self._det is None:
            from linguonnx import load_detector
            logger.info("Loading glotlid detector (first call downloads ~419 MB)...")
            self._det = load_detector()
        return self._det

    def detect(
        self, text: str, top_k: int = 5
    ) -> List[Tuple[str, float]]:
        """
        Return list of (label, confidence) tuples, highest first.
        Never raises — returns [] on failure.
        """
        if not text or not text.strip():
            return []
        try:
            det = self._load()
            probs = det.detect_probs(text, top_k=top_k)
            if isinstance(probs, dict):
                items = sorted(probs.items(), key=lambda x: x[1], reverse=True)
            else:
                items = list(probs)
            return items
        except Exception as e:
            logger.warning(f"Language detection failed: {e}")
            return []

    def detect_top(self, text: str) -> Tuple[Optional[str], Optional[str], float]:
        """
        Convenience: return (raw_label, iso_code, confidence) for top guess.
        Returns (None, None, 0.0) if detection fails.
        """
        probs = self.detect(text, top_k=1)
        if not probs:
            return None, None, 0.0
        raw_label, conf = probs[0]
        iso = normalize_lang_code(raw_label.split("-")[0])
        return raw_label, iso, float(conf)


# ----------------------------------------------------------------------
# Functional convenience API
# ----------------------------------------------------------------------
_DEFAULT_DETECTOR: Optional[LanguageDetector] = None


def _get_default_detector() -> LanguageDetector:
    global _DEFAULT_DETECTOR
    if _DEFAULT_DETECTOR is None:
        _DEFAULT_DETECTOR = LanguageDetector()
    return _DEFAULT_DETECTOR


def detect(text: str, k: int = 1):
    """Return top-k detection as a list of (label, confidence)."""
    return _get_default_detector().detect(text, top_k=k)


def detect_language(text: str):
    """Return (raw_label, iso_code, confidence) for the top guess."""
    return _get_default_detector().detect_top(text)


# ----------------------------------------------------------------------
# Interactive CLI
# ----------------------------------------------------------------------
def main():
    print("=" * 70)
    print("Language Detector (glotlid) — enter text to identify its language.")
    print("Type 'quit' or 'exit' (or Ctrl+C) to stop.")
    print("=" * 70)

    while True:
        try:
            user_input = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not user_input:
            continue
        if user_input.lower() in {"quit", "exit"}:
            print("Bye!")
            break

        results = detect(user_input, k=5)
        if not results:
            print("No detection result.")
            continue

        print("\nTop predictions:")
        for label, conf in results:
            iso = normalize_lang_code(label.split("-")[0])
            print(f"  {label:<20} → {iso:<6} conf={conf:.4f}")


if __name__ == "__main__":
    main()