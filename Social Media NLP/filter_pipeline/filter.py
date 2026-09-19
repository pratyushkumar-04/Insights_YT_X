"""
filter_pipeline.py
------------------
Standalone filter pipeline — applies ONLY:
    1. Spam filter
    2. Relevance filter (title ↔ comment, any-metric >= threshold)
    3. Harmful filter

No normalization, no script/language detection, no transliteration.

Run:
    python filter_pipeline.py
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional

from spam_filter import SpamFilter
from relevance_filter import RelevanceFilter
from harmful_filter import HarmfulFilter


# ----------------------------------------------------------------------
# Result container — everything the caller needs
# ----------------------------------------------------------------------
@dataclass
class FilterResult:
    title: Optional[str]
    comment: str

    # Spam
    is_spam: Optional[bool] = None
    spam_label: Optional[str] = None

    # Relevance
    is_relevant: Optional[bool] = None
    relevance_threshold: Optional[float] = None
    relevance_passed_metrics: List[str] = field(default_factory=list)
    relevance_metrics: Dict[str, float] = field(default_factory=dict)

    # Harmful
    is_harmful: Optional[bool] = None
    harmful_label: Optional[str] = None

    # Step diagnostics
    steps_applied: Dict[str, bool] = field(default_factory=dict)

    @property
    def should_publish(self) -> bool:
        """
        Accept only if: not spam AND relevant AND not harmful.
        Treats a skipped relevance step (no title given) as neutral.
        """
        ok_spam = self.is_spam is not True
        ok_relevance = self.is_relevant is not False
        ok_harmful = self.is_harmful is not True
        return ok_spam and ok_relevance and ok_harmful

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["should_publish"] = self.should_publish
        return d


# ----------------------------------------------------------------------
# The pipeline
# ----------------------------------------------------------------------
class FilterPipeline:
    """
    Applies spam → relevance → harmful in that order.

    Parameters
    ----------
    run_spam, run_relevance, run_harmful : bool
        Toggle individual filters.
    relevance_threshold : float
        Any-pass threshold for the relevance filter (default 0.15).
    relevance_model : str
        Sentence-transformer model name.
    """

    def __init__(
        self,
        *,
        run_spam: bool = True,
        run_relevance: bool = True,
        run_harmful: bool = True,
        relevance_threshold: float = 0.15,
        relevance_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        self.do_spam = run_spam
        self.do_relevance = run_relevance
        self.do_harmful = run_harmful
        self._relevance_threshold = relevance_threshold
        self._relevance_model = relevance_model

        self._spam_filter: Optional[SpamFilter] = None
        self._relevance_filter: Optional[RelevanceFilter] = None
        self._harmful_filter: Optional[HarmfulFilter] = None

    # ----- lazy getters -----
    @property
    def spam_filter(self) -> SpamFilter:
        if self._spam_filter is None:
            self._spam_filter = SpamFilter()
        return self._spam_filter

    @property
    def relevance_filter(self) -> RelevanceFilter:
        if self._relevance_filter is None:
            self._relevance_filter = RelevanceFilter(
                model_name=self._relevance_model,
                threshold=self._relevance_threshold,
            )
        return self._relevance_filter

    @property
    def harmful_filter(self) -> HarmfulFilter:
        if self._harmful_filter is None:
            self._harmful_filter = HarmfulFilter()
        return self._harmful_filter

    # ----- main entry -----
    def run(self, comment: str, title: Optional[str] = None) -> FilterResult:
        result = FilterResult(title=title, comment=comment)

        if not isinstance(comment, str) or not comment.strip():
            return result

        # ---------- 1. Spam ----------
        if self.do_spam:
            try:
                sr = self.spam_filter.classify(comment)
                result.is_spam = sr.is_spam
                result.spam_label = sr.label
                result.steps_applied["spam"] = True
            except Exception as e:
                print(f"[pipeline] spam step failed: {e}")
                result.steps_applied["spam"] = False

        # ---------- 2. Relevance ----------
        if self.do_relevance and title:
            try:
                rr = self.relevance_filter.evaluate(title, comment)
                result.is_relevant = rr.is_relevant
                result.relevance_threshold = rr.threshold
                result.relevance_passed_metrics = list(rr.passed_metrics)
                result.relevance_metrics = dict(rr.metrics)
                result.steps_applied["relevance"] = True
            except Exception as e:
                print(f"[pipeline] relevance step failed: {e}")
                result.steps_applied["relevance"] = False
        else:
            result.steps_applied["relevance"] = False

        # ---------- 3. Harmful ----------
        if self.do_harmful:
            try:
                hr = self.harmful_filter.classify(comment)
                result.is_harmful = hr.is_harmful
                result.harmful_label = hr.label
                result.steps_applied["harmful"] = True
            except Exception as e:
                print(f"[pipeline] harmful step failed: {e}")
                result.steps_applied["harmful"] = False

        return result


# ----------------------------------------------------------------------
# Functional convenience
# ----------------------------------------------------------------------
_DEFAULT_PIPELINE: Optional[FilterPipeline] = None


def filter_comment(
    comment: str,
    title: Optional[str] = None,
    **overrides,
) -> FilterResult:
    global _DEFAULT_PIPELINE
    if _DEFAULT_PIPELINE is None or overrides:
        _DEFAULT_PIPELINE = FilterPipeline(**overrides)
    return _DEFAULT_PIPELINE.run(comment, title=title)


# ----------------------------------------------------------------------
# Pretty printing
# ----------------------------------------------------------------------
def _fmt_bool(v: Optional[bool]) -> str:
    if v is None:
        return "—"
    return "YES" if v else "NO"


def _pretty(r: FilterResult) -> str:
    lines = [
        "─" * 70,
        f"Comment      : {r.comment}",
        f"Title        : {r.title if r.title else '(none — relevance skipped)'}",
        "─" * 70,
        "FILTERS",
        f"  Spam      : {_fmt_bool(r.is_spam)}"
        + (f"  ({r.spam_label})" if r.spam_label else ""),
        f"  Relevant  : {_fmt_bool(r.is_relevant)}"
        + (
            f"  (threshold={r.relevance_threshold}, "
            f"passed={r.relevance_passed_metrics})"
            if r.relevance_threshold is not None
            else ""
        ),
        f"  Harmful   : {_fmt_bool(r.is_harmful)}"
        + (f"  ({r.harmful_label})" if r.harmful_label else ""),
        "─" * 70,
        f"SHOULD PUBLISH : {_fmt_bool(r.should_publish)}",
        "─" * 70,
    ]

    if r.relevance_metrics:
        lines.append("Relevance metrics:")
        for k, v in r.relevance_metrics.items():
            mark = "PASS" if k in r.relevance_passed_metrics else "    "
            lines.append(f"  [{mark}] {k:<22} {v:+.4f}")
        lines.append("─" * 70)

    return "\n".join(lines)


# ----------------------------------------------------------------------
# Interactive CLI
# ----------------------------------------------------------------------
def main():
    print("=" * 70)
    print("Filter Pipeline — spam → relevance → harmful")
    print("Commands:")
    print("  :title <text>     set/change the post title (needed for relevance)")
    print("  :thr <float>      set relevance threshold (default 0.15)")
    print("  :off <step>       step = spam|relevance|harmful")
    print("  quit / exit")
    print("=" * 70)

    pipeline = FilterPipeline()
    current_title: Optional[str] = None

    print("\nOptional: enter a post title first (blank to skip relevance).")
    try:
        current_title = input("Post title > ").strip() or None
    except (EOFError, KeyboardInterrupt):
        print("\nBye!")
        return

    while True:
        try:
            user_input = input("\nComment > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not user_input:
            continue
        if user_input.lower() in {"quit", "exit"}:
            print("Bye!")
            break

        # --- runtime commands ---
        if user_input.startswith(":title "):
            current_title = user_input.split(maxsplit=1)[1].strip()
            print(f"[title = {current_title}]")
            continue
        if user_input.startswith(":thr "):
            try:
                thr = float(user_input.split(maxsplit=1)[1])
                pipeline._relevance_threshold = thr
                pipeline._relevance_filter = None  # force rebuild with new threshold
                print(f"[relevance threshold = {thr}]")
            except ValueError:
                print("Usage: :thr 0.20")
            continue
        if user_input.startswith(":off "):
            step = user_input.split(maxsplit=1)[1].strip()
            mapping = {
                "spam": "do_spam",
                "relevance": "do_relevance",
                "harmful": "do_harmful",
            }
            attr = mapping.get(step)
            if attr:
                setattr(pipeline, attr, not getattr(pipeline, attr))
                print(f"[{attr} = {getattr(pipeline, attr)}]")
            else:
                print(f"Unknown step: {step}")
            continue

        # --- run pipeline ---
        try:
            result = pipeline.run(user_input, title=current_title)
            print(_pretty(result))
        except Exception as e:
            print(f"[Error] {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()