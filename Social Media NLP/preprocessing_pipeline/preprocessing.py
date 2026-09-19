"""
pipeline.py
-----------
Unified preprocessing pipeline for Indic/NLP text.

Order of operations:
    1. Text normalization  (text_normalization.TextNormalizer)
    2. Script detection    (script_detection.analyze_text)
    3. Language detection  (language_detection.LanguageDetector / glotlid)
    4. Transliteration     (transliteration.transliterate, optional)

Metadata is carried forward in a ProcessedResult dataclass so downstream
stages can branch on script, language, and whether transliteration happened.

Usage:
    from pipeline import preprocess
    result = preprocess("Video bahut badhia heichi.. banei chala!!!")
    print(result.final_text)
    print(result.to_dict())
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional

# ----------------------------------------------------------------------
# Local module imports
# ----------------------------------------------------------------------
from text_normalization import TextNormalizer
from script_detection import analyze_text
from language_detection import LanguageDetector, normalize_lang_code
from transliteration import transliterate, INDIC_XLIT_LANGS

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger("preprocess")


# ----------------------------------------------------------------------
# Result container — everything downstream needs
# ----------------------------------------------------------------------
@dataclass
class ProcessedResult:
    """Carries text + metadata through the preprocessing pipeline."""

    # Text at each stage
    original_text: str
    normalized_text: str
    final_text: str

    # Script detection
    primary_script: Optional[str] = None
    mixed_script: bool = False
    script_distribution: Dict[str, int] = field(default_factory=dict)

    # Language detection
    detected_language_raw: Optional[str] = None      # e.g. "hin_Deva"
    detected_language_code: Optional[str] = None     # e.g. "hi"
    language_confidence: float = 0.0

    # Transliteration
    was_transliterated: bool = False
    transliteration_target: Optional[str] = None     # e.g. "hi", "or"

    # Free-form extras for future stages
    extras: Dict[str, Any] = field(default_factory=dict)

    # Step-level flags (useful for debugging / conditional downstream logic)
    steps_applied: Dict[str, bool] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ----------------------------------------------------------------------
# The pipeline
# ----------------------------------------------------------------------
class PreprocessingPipeline:
    """
    End-to-end preprocessing pipeline.

    Parameters
    ----------
    normalize : bool
        Run TextNormalizer.
    detect_script : bool
        Run script analyzer.
    detect_language : bool
        Run glotlid language detection.
    transliterate_romanized : bool
        If primary script is Latin AND detected language is Indic,
        attempt transliteration to native script.
    forced_lang : Optional[str]
        If provided, skip language detection and use this language code.
    normalizer_kwargs : dict
        Passed through to TextNormalizer constructor.
    translit_device : str
        "cpu" or "cuda" for the CT2 translator.
    translit_beam_size : int
        Beam size for transliteration.
    """

    INDIC_ROMANIZED_HINTS = {
        "hi", "bn", "or", "ta", "te", "mr", "gu",
        "kn", "ml", "pa", "as", "ur", "ne", "si",
    }

    def __init__(
        self,
        *,
        normalize: bool = True,
        detect_script: bool = True,
        detect_language: bool = True,
        transliterate_romanized: bool = True,
        forced_lang: Optional[str] = None,
        normalizer_kwargs: Optional[dict] = None,
        translit_device: str = "cpu",
        translit_beam_size: int = 4,
    ):
        self.do_normalize = normalize
        self.do_script = detect_script
        self.do_lang = detect_language
        self.do_translit = transliterate_romanized
        self.forced_lang = forced_lang
        self.translit_device = translit_device
        self.translit_beam_size = translit_beam_size

        self.normalizer = TextNormalizer(**(normalizer_kwargs or {}))
        self.lang_detector = LanguageDetector()

    # ------------------------------------------------------------------
    def run(self, text: str) -> ProcessedResult:
        result = ProcessedResult(
            original_text=text,
            normalized_text=text,
            final_text=text,
        )

        if not isinstance(text, str) or not text.strip():
            return result

        # ---------- Step 1: Normalization ----------
        working = text
        if self.do_normalize:
            try:
                working = self.normalizer.normalize(text)
                result.steps_applied["normalize"] = True
            except Exception as e:
                logger.warning(f"Normalization failed: {e}")
                working = text
                result.steps_applied["normalize"] = False
        result.normalized_text = working

        # ---------- Step 2: Script detection ----------
        if self.do_script:
            try:
                analysis = analyze_text(working)
                result.primary_script = analysis.get("primary")
                result.mixed_script = analysis.get("mixed", False)
                result.script_distribution = dict(analysis.get("scripts", {}))
                result.steps_applied["script"] = True
            except Exception as e:
                logger.warning(f"Script detection failed: {e}")
                result.steps_applied["script"] = False

        # ---------- Step 3: Language detection ----------
        if self.forced_lang:
            result.detected_language_code = normalize_lang_code(self.forced_lang)
            result.detected_language_raw = self.forced_lang
            result.language_confidence = 1.0
            result.steps_applied["lang"] = False  # skipped (forced)
        elif self.do_lang:
            try:
                probs = self.lang_detector.detect(working, top_k=5)
                if probs:
                    raw_label, conf = probs[0]
                    result.detected_language_raw = raw_label
                    result.detected_language_code = normalize_lang_code(
                        raw_label.split("-")[0]
                    )
                    result.language_confidence = float(conf)
                    result.extras["lang_top_k"] = probs
                    result.steps_applied["lang"] = True
                else:
                    result.steps_applied["lang"] = False
            except Exception as e:
                logger.warning(f"Language detection failed: {e}")
                result.steps_applied["lang"] = False

        # ---------- Step 4: Transliteration (conditional) ----------
        should_translit = (
            self.do_translit
            and result.primary_script == "Latin"
            and result.detected_language_code in self.INDIC_ROMANIZED_HINTS
        )

        if should_translit:
            try:
                native = transliterate(
                    working,
                    lang=result.detected_language_code,
                    beam_size=self.translit_beam_size,
                    device=self.translit_device,
                )
                if native and native != working:
                    result.final_text = native
                    result.was_transliterated = True
                    result.transliteration_target = result.detected_language_code
                    result.steps_applied["translit"] = True
                else:
                    result.final_text = working
                    result.steps_applied["translit"] = False
            except Exception as e:
                logger.warning(f"Transliteration failed: {e}")
                result.final_text = working
                result.steps_applied["translit"] = False
        else:
            result.final_text = working
            result.steps_applied["translit"] = False

        return result


# ----------------------------------------------------------------------
# Convenience functional API
# ----------------------------------------------------------------------
_DEFAULT_PIPELINE: Optional[PreprocessingPipeline] = None


def preprocess(text: str, **overrides) -> ProcessedResult:
    """
    One-shot convenience wrapper using a module-level default pipeline.
    Pass overrides like forced_lang="hi" or transliterate_romanized=False.
    """
    global _DEFAULT_PIPELINE
    if _DEFAULT_PIPELINE is None or overrides:
        _DEFAULT_PIPELINE = PreprocessingPipeline(**overrides)
    return _DEFAULT_PIPELINE.run(text)


# ----------------------------------------------------------------------
# Pretty printing
# ----------------------------------------------------------------------
def _pretty(result: ProcessedResult) -> str:
    lines = [
        "─" * 70,
        f"Original        : {result.original_text}",
        f"Normalized      : {result.normalized_text}",
        f"Primary script  : {result.primary_script}  (mixed={result.mixed_script})",
        f"Script dist.    : {result.script_distribution}",
        f"Language (raw)  : {result.detected_language_raw}  "
        f"(conf={result.language_confidence:.3f})",
        f"Language (ISO)  : {result.detected_language_code}",
        f"Transliterated  : {result.was_transliterated} "
        f"(→ {result.transliteration_target})",
        f"FINAL TEXT      : {result.final_text}",
        "─" * 70,
    ]
    return "\n".join(lines)


# ----------------------------------------------------------------------
# Interactive CLI
# ----------------------------------------------------------------------
def main():
    print("=" * 70)
    print("Preprocessing Pipeline — normalize → script → language → translit")
    print("Commands:  :lang <code>  (force language)   :notrans  (toggle translit)")
    print("           :off <step>   (step = normalize|script|lang|translit)")
    print("           quit / exit")
    print("=" * 70)

    pipeline = PreprocessingPipeline()

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

        # --- runtime toggles ---
        if user_input.startswith(":lang "):
            pipeline.forced_lang = user_input.split(maxsplit=1)[1].strip()
            print(f"[forced_lang = {pipeline.forced_lang}]")
            continue
        if user_input == ":notrans":
            pipeline.do_translit = not pipeline.do_translit
            print(f"[transliterate_romanized = {pipeline.do_translit}]")
            continue
        if user_input.startswith(":off "):
            step = user_input.split(maxsplit=1)[1].strip()
            mapping = {
                "normalize": "do_normalize",
                "script": "do_script",
                "lang": "do_lang",
                "translit": "do_translit",
            }
            attr = mapping.get(step)
            if attr:
                setattr(pipeline, attr, not getattr(pipeline, attr))
                print(f"[{attr} = {getattr(pipeline, attr)}]")
            else:
                print(f"Unknown step: {step}")
            continue

        try:
            result = pipeline.run(user_input)
            print(_pretty(result))
        except Exception as e:
            print(f"[Error] {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()