"""
transliterate_indic.py
----------------------
Convert romanized Indic text to native script.

Usage:
    from transliterate_indic import transliterate
    native = transliterate("Video bahut badhia heichi.. banei chala!!!")

Install:
    pip install linguonnx ctranslate2 huggingface_hub
"""

from __future__ import annotations

import logging
import re
import warnings
from typing import Optional

logging.getLogger("langcodes").setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=UserWarning, module="langcodes")


INDIC_XLIT_LANGS = {
    "as", "bn", "brx", "gu", "hi", "kn", "ks", "gom", "mai", "ml",
    "mni", "mr", "ne", "or", "pa", "sa", "sd", "si", "ta", "te", "ur",
}

LANG_ALIASES = {
    "ory": "or", "ori": "or", "pan": "pa", "san": "sa", "snd": "sd",
    "sin": "si", "tam": "ta", "tel": "te", "urd": "ur", "mal": "ml",
    "kan": "kn", "guj": "gu", "mar": "mr", "nep": "ne", "ben": "bn",
    "asm": "as", "hin": "hi",
}

FALLBACK_LANGS = ("hi", "or", "bn", "ta", "te", "mr", "gu", "kn", "ml", "pa")


def normalize_lang_code(code: str) -> str:
    base = code.split("-")[0].split("_")[0].lower()
    return LANG_ALIASES.get(base, base)


_WORD_RE = re.compile(r"[A-Za-z]+")
_HF_REPO = "Singla0009/all-indic-transliteration"
_SUBFOLDER = "indicxlit_ct2_fp32"

_detector = None
_ct2_translator = None


def _get_detector():
    global _detector
    if _detector is None:
        from linguonnx import load_detector
        _detector = load_detector()
    return _detector


def _get_ct2_translator(device: str = "cpu"):
    global _ct2_translator
    if _ct2_translator is None:
        import os
        import ctranslate2
        from huggingface_hub import snapshot_download

        model_path = snapshot_download(
            repo_id=_HF_REPO, allow_patterns=f"{_SUBFOLDER}/*"
        )
        model_dir = os.path.join(model_path, _SUBFOLDER)
        _ct2_translator = ctranslate2.Translator(model_dir, device=device)
    return _ct2_translator


def _transliterate_text(text: str, lang_code: str, beam_size: int = 4,
                        device: str = "cpu") -> str:
    matches = list(_WORD_RE.finditer(text))
    if not matches:
        return text

    translator = _get_ct2_translator(device=device)
    words = [m.group() for m in matches]
    batch = [[f"__{lang_code}__"] + list(w) for w in words]
    results = translator.translate_batch(batch, beam_size=beam_size)
    outputs = ["".join(r.hypotheses[0]) for r in results]

    pieces = []
    last = 0
    for m, out in zip(matches, outputs):
        pieces.append(text[last:m.start()])
        pieces.append(out)
        last = m.end()
    pieces.append(text[last:])
    return "".join(pieces)


def _detect_lang(text: str):
    try:
        det = _get_detector()
    except Exception:
        return None, None, 0.0

    try:
        probs = det.detect_probs(text, top_k=5)
    except TypeError:
        probs = det.detect_probs(text)

    if not probs:
        return None, None, 0.0

    for raw_label, conf in probs.items():
        code = normalize_lang_code(raw_label.split("-")[0])
        if code in INDIC_XLIT_LANGS:
            return raw_label, code, float(conf)

    raw_label, conf = next(iter(probs.items()))
    return raw_label, normalize_lang_code(raw_label.split("-")[0]), float(conf)


def _looks_romanized(text: str, threshold: float = 0.5) -> bool:
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return False
    return sum(1 for c in letters if c.isascii()) / len(letters) >= threshold


def transliterate(
    text: str,
    lang: Optional[str] = None,
    *,
    min_conf: float = 0.05,
    beam_size: int = 4,
    device: str = "cpu",
) -> str:
    """Convert romanized Indic text to native script. Never raises."""
    if not isinstance(text, str) or not text.strip():
        return text

    if not _looks_romanized(text, threshold=0.5):
        return text

    if lang is not None:
        lang_code = normalize_lang_code(lang)
    else:
        _raw, lang_code, conf = _detect_lang(text)
        if lang_code is None or conf < min_conf:
            lang_code = None

    if lang_code in INDIC_XLIT_LANGS:
        try:
            result = _transliterate_text(
                text, lang_code, beam_size=beam_size, device=device
            )
            if result != text:
                return result
        except Exception:
            pass

    for fallback in FALLBACK_LANGS:
        try:
            result = _transliterate_text(
                text, fallback, beam_size=beam_size, device=device
            )
            if result != text:
                return result
        except Exception:
            continue

    return text


if __name__ == "__main__":
    user_input = input("Enter text: ").strip()
    if user_input:
        print(transliterate(user_input))