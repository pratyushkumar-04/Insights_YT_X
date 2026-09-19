import unicodedata
import re
from collections import Counter


# ----------------------------------------------------------------------
# Unicode script ranges
# Each entry: (script_name, [(start_cp, end_cp), ...])
# Ranges chosen to cover the "meaningful" (non-Common / non-Inherited)
# scripts you'll typically encounter. Order matters only for readability.
# ----------------------------------------------------------------------
SCRIPT_RANGES = [
    ("Latin", [
        (0x0041, 0x005A), (0x0061, 0x007A),           # Basic Latin letters
        (0x00C0, 0x00FF),                              # Latin-1 Supplement letters
        (0x0100, 0x017F),                              # Latin Extended-A
        (0x0180, 0x024F),                              # Latin Extended-B
        (0x1E00, 0x1EFF),                              # Latin Extended Additional
        (0x2C60, 0x2C7F),                              # Latin Extended-C
        (0xA720, 0xA7FF),                              # Latin Extended-D
    ]),
    ("Devanagari", [
        (0x0900, 0x097F),                              # Devanagari
        (0xA8E0, 0xA8FF),                              # Devanagari Extended
        (0x1CD0, 0x1CFF),                              # Vedic Extensions
    ]),
    ("Bengali", [
        (0x0980, 0x09FF),                              # Bengali
    ]),
    ("Gurmukhi", [
        (0x0A00, 0x0A7F),
    ]),
    ("Gujarati", [
        (0x0A80, 0x0AFF),
    ]),
    ("Oriya", [
        (0x0B00, 0x0B7F),
    ]),
    ("Tamil", [
        (0x0B80, 0x0BFF),
    ]),
    ("Telugu", [
        (0x0C00, 0x0C7F),
    ]),
    ("Kannada", [
        (0x0C80, 0x0CFF),
    ]),
    ("Malayalam", [
        (0x0D00, 0x0D7F),
    ]),
    ("Sinhala", [
        (0x0D80, 0x0DFF),
    ]),
    ("Thai", [
        (0x0E00, 0x0E7F),
    ]),
    ("Lao", [
        (0x0E80, 0x0EFF),
    ]),
    ("Tibetan", [
        (0x0F00, 0x0FFF),
    ]),
    ("Myanmar", [
        (0x1000, 0x109F),
    ]),
    ("Georgian", [
        (0x10A0, 0x10FF),
    ]),
    ("Hangul", [
        (0x1100, 0x11FF),                              # Jamo
        (0xAC00, 0xD7AF),                              # Syllables
        (0x3130, 0x318F),                              # Compatibility Jamo
    ]),
    ("Ethiopic", [
        (0x1200, 0x137F),
    ]),
    ("Cherokee", [
        (0x13A0, 0x13FF),
    ]),
    ("Khmer", [
        (0x1780, 0x17FF),
    ]),
    ("Mongolian", [
        (0x1800, 0x18AF),
    ]),
    ("Hiragana", [
        (0x3040, 0x309F),
    ]),
    ("Katakana", [
        (0x30A0, 0x30FF),
        (0x31F0, 0x31FF),                              # Katakana Phonetic Extensions
    ]),
    ("Bopomofo", [
        (0x3100, 0x312F),
    ]),
    ("CJK", [
        (0x4E00, 0x9FFF),                              # CJK Unified Ideographs
        (0x3400, 0x4DBF),                              # Extension A
        (0x20000, 0x2A6DF),                            # Extension B
        (0xF900, 0xFAFF),                              # Compatibility Ideographs
    ]),
    ("Arabic", [
        (0x0600, 0x06FF),                              # Arabic
        (0x0750, 0x077F),                              # Arabic Supplement
        (0x08A0, 0x08FF),                              # Arabic Extended-A
        (0xFB50, 0xFDFF),                              # Arabic Presentation Forms-A
        (0xFE70, 0xFEFF),                              # Arabic Presentation Forms-B
    ]),
    ("Hebrew", [
        (0x0590, 0x05FF),
        (0xFB1D, 0xFB4F),                              # Hebrew Presentation Forms
    ]),
    ("Syriac", [
        (0x0700, 0x074F),
    ]),
    ("Thaana", [
        (0x0780, 0x07BF),
    ]),
    ("Greek", [
        (0x0370, 0x03FF),
        (0x1F00, 0x1FFF),                              # Greek Extended
    ]),
    ("Cyrillic", [
        (0x0400, 0x04FF),
        (0x0500, 0x052F),                              # Cyrillic Supplement
        (0x2DE0, 0x2DFF),                              # Cyrillic Extended-A
        (0xA640, 0xA69F),                              # Cyrillic Extended-B
    ]),
    ("Armenian", [
        (0x0530, 0x058F),
    ]),
    ("Runic", [
        (0x16A0, 0x16FF),
    ]),
]


def _build_lookup():
    """Flatten SCRIPT_RANGES into a sorted list of (start, end, script) for fast lookup."""
    lookup = []
    for script, ranges in SCRIPT_RANGES:
        for start, end in ranges:
            lookup.append((start, end, script))
    lookup.sort(key=lambda x: x[0])
    return lookup


_SCRIPT_LOOKUP = _build_lookup()


def identify_script(char: str):
    """
    Return the script name for a single character, or None for
    Common / Inherited / unassigned characters (digits, punctuation,
    whitespace, emoji, combining marks, etc.).
    """
    cp = ord(char)
    for start, end, script in _SCRIPT_LOOKUP:
        if start <= cp <= end:
            return script
    return None


def analyze_text(text: str):
    """
    Return a structured analysis of the scripts present in `text`.

    Returns a dict with:
      - 'scripts': Counter {script_name: count}
      - 'primary': most frequent script, or None if no script chars found
      - 'mixed':   True if 2+ distinct scripts are present (excluding Common)
      - 'per_char': list of (char, script_or_None) for inspection
    """
    counts = Counter()
    per_char = []

    for ch in text:
        # Skip whitespace and control chars — they carry no script info
        if ch.isspace():
            per_char.append((ch, None))
            continue

        # Skip combining marks (they belong to the preceding base char's script)
        if unicodedata.category(ch).startswith("M"):
            per_char.append((ch, None))
            continue

        script = identify_script(ch)
        per_char.append((ch, script))
        if script:
            counts[script] += 1

    primary = counts.most_common(1)[0][0] if counts else None
    mixed = len(counts) > 1

    return {
        "scripts": counts,
        "primary": primary,
        "mixed": mixed,
        "per_char": per_char,
    }


def format_report(text: str) -> str:
    """Pretty-print the script analysis."""
    analysis = analyze_text(text)
    counts = analysis["scripts"]
    primary = analysis["primary"]
    mixed = analysis["mixed"]

    total = sum(counts.values())

    lines = []
    lines.append(f"Text length (code points): {len(text)}")
    lines.append(f"Script-bearing characters: {total}")

    if not counts:
        lines.append("No identifiable script found (only punctuation/digits/emoji?).")
        return "\n".join(lines)

    lines.append(f"Primary script: {primary}")
    lines.append(f"Mixed script: {mixed}")
    lines.append("")
    lines.append("Script distribution:")

    for script, count in counts.most_common():
        pct = (count / total) * 100
        bar = "█" * max(1, int(pct / 5))  # 1 block per 5%
        lines.append(f"  {script:<12} {count:>5}  ({pct:5.1f}%)  {bar}")

    # Show which characters belong to which script (compact)
    lines.append("")
    lines.append("Per-character script tags (· = Common/None):")
    tokens = []
    for ch, script in analysis["per_char"]:
        if ch.isspace():
            tokens.append("·")
        elif script:
            tokens.append(f"{ch}⟨{script[:3]}⟩")
        else:
            tokens.append(f"{ch}⟨·⟩")
    lines.append("  " + " ".join(tokens))

    return primary


# ----------------------------------------------------------------------
# Interactive CLI
# ----------------------------------------------------------------------
def main():
    print("=" * 70)
    print("Script Detector — enter text to identify its writing system(s).")
    print("Type 'quit' or 'exit' (or Ctrl+C) to stop.")
    print("=" * 70)

    # A few self-test examples printed once
    print("\nExamples you can paste:")
    print("  मुझे पसंद है")
    print("  বাংলা ভাষা")
    print("  தமிழ்")
    print("  Hello, world!")
    print("  العربية")
    print("  Hello दुनिया — mixed!")
    print()

    while True:
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not user_input:
            continue

        if user_input.lower() in {"quit", "exit"}:
            print("Bye!")
            break

        print()
        print(format_report(user_input))
        print("-" * 70)


if __name__ == "__main__":
    main()