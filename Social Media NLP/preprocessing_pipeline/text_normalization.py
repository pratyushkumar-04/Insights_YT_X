"""
text_normalization.py
---------------------
Text cleaning and normalization for NLP preprocessing.
"""

import re
import unicodedata
import html
from urllib.parse import urlparse, urlunparse
from bs4 import BeautifulSoup

# Optional: pip install emoji
try:
    import emoji
    EMOJI_AVAILABLE = True
except ImportError:
    EMOJI_AVAILABLE = False


class TextNormalizer:
    def __init__(
        self,
        unicode_form="NFC",          # "NFC" or "NFKC"
        max_char_repeat=2,            # keep at most N letter/digit repeats
        max_punct_repeat=1,           # keep at most N punctuation repeats
        lowercase=True,
        remove_urls=False,            # True = remove URLs, False = keep them
        normalize_urls=True,          # strip tracking params (utm_*)
        strip_html=True,
        preserve_emojis=True,
        collapse_whitespace=True,
    ):
        self.unicode_form = unicode_form
        self.max_char_repeat = max_char_repeat
        self.max_punct_repeat = max_punct_repeat
        self.lowercase = lowercase
        self.remove_urls = remove_urls
        self.normalize_urls = normalize_urls
        self.strip_html = strip_html
        self.preserve_emojis = preserve_emojis
        self.collapse_whitespace = collapse_whitespace

        # Regex patterns
        self.url_pattern = re.compile(
            r'((?:https?://|www\.)[^\s<>"\']+|'
            r'\b[a-zA-Z0-9.-]+\.(?:com|org|net|io|gov|edu|co|in|uk|de|jp|ai|app)(?:/[^\s<>"\']*)?)',
            re.IGNORECASE,
        )
        self.html_tag_pattern = re.compile(r'<[^>]+>')
        self.control_chars_pattern = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]')

        # Trackable URL query params to strip
        self.tracking_params = re.compile(
            r'^(utm_|fbclid|gclid|mc_eid|mc_cid|ref|igshid|si)$',
            re.IGNORECASE,
        )

        # Emoji placeholder (private-use area) for protection during processing
        self._emoji_placeholder = "\uE000"
        self._emoji_store = {}

    # ---------- Step 1: Unicode normalization ----------
    def normalize_unicode(self, text: str) -> str:
        return unicodedata.normalize(self.unicode_form, text)

    # ---------- Step 2: HTML / entity cleanup ----------
    def clean_html(self, text: str) -> str:
        text = html.unescape(text)
        if self.strip_html:
            if self.html_tag_pattern.search(text):
                soup = BeautifulSoup(text, "html.parser")
                text = soup.get_text(separator=" ")
        text = self.control_chars_pattern.sub("", text)
        return text

    # ---------- Step 3: Protect emojis ----------
    def _protect_emojis_manual(self, text: str) -> str:
        if not self.preserve_emojis:
            return text

        emoji_pattern = re.compile(
            "["
            "\U0001F300-\U0001F5FF"
            "\U0001F600-\U0001F64F"
            "\U0001F680-\U0001F6FF"
            "\U0001F700-\U0001F77F"
            "\U0001F780-\U0001F7FF"
            "\U0001F800-\U0001F8FF"
            "\U0001F900-\U0001F9FF"
            "\U0001FA00-\U0001FAFF"
            "\U00002700-\U000027BF"
            "\U00002600-\U000026FF"
            "\U0001F1E0-\U0001F1FF"
            "\U0000FE00-\U0000FE0F"
            "\U0000200D"
            "]+",
            flags=re.UNICODE,
        )

        self._emoji_store = {}

        def repl(match):
            key = f"{self._emoji_placeholder}{len(self._emoji_store)}{self._emoji_placeholder}"
            self._emoji_store[key] = match.group(0)
            return key

        return emoji_pattern.sub(repl, text)

    def _restore_emojis(self, text: str) -> str:
        if not self.preserve_emojis or not self._emoji_store:
            return text
        for key, val in self._emoji_store.items():
            text = text.replace(key, val)
        return text

    # ---------- Step 4: URL handling ----------
    def handle_urls(self, text: str) -> str:
        def process(match):
            url = match.group(0)
            if self.remove_urls:
                return " "
            if not self.normalize_urls:
                return url

            prefixed = url if url.startswith(("http://", "https://")) else "http://" + url
            try:
                parsed = urlparse(prefixed)
                if parsed.query:
                    kept = [
                        kv for kv in parsed.query.split("&")
                        if not self.tracking_params.match(kv.split("=")[0])
                    ]
                    new_query = "&".join(kept)
                else:
                    new_query = ""

                cleaned = urlunparse((
                    parsed.scheme,
                    parsed.netloc,
                    parsed.path,
                    parsed.params,
                    new_query,
                    "",
                ))
                if not url.startswith(("http://", "https://")):
                    cleaned = cleaned.replace("http://", "", 1)
                return cleaned
            except Exception:
                return url

        return self.url_pattern.sub(process, text)

    # ---------- Step 5: Repeated character + punctuation collapsing ----------
    def collapse_repeats(self, text: str) -> str:
        if self.max_char_repeat > 0:
            char_pattern = re.compile(
                r'(\w)\1{' + str(self.max_char_repeat) + r',}',
                flags=re.UNICODE,
            )
            text = char_pattern.sub(
                lambda m: m.group(1) * self.max_char_repeat, text
            )

        if self.max_punct_repeat > 0:
            punct_pattern = re.compile(
                r'([?!.,;:\-])\1{' + str(self.max_punct_repeat) + r',}'
            )
            text = punct_pattern.sub(
                lambda m: m.group(1) * self.max_punct_repeat, text
            )

        return text

    # ---------- Step 6: Special symbols ----------
    def clean_symbols(self, text: str) -> str:
        replacements = {
            "\u2018": "'", "\u2019": "'",
            "\u201C": '"', "\u201D": '"',
            "\u2013": "-", "\u2014": "-",
            "\u2026": "...",
            "\u00A0": " ",
            "\u200B": "",
            "\uFEFF": "",
        }
        for k, v in replacements.items():
            text = text.replace(k, v)
        return text

    # ---------- Step 7: Whitespace cleanup ----------
    def clean_whitespace(self, text: str) -> str:
        if self.collapse_whitespace:
            text = re.sub(r"\s+", " ", text)
        text = text.strip()
        return text

    # ---------- Step 8: Case normalization ----------
    def normalize_case(self, text: str) -> str:
        if self.lowercase:
            return text.lower()
        return text

    # ---------- Full pipeline ----------
    def normalize(self, text: str) -> str:
        if not isinstance(text, str) or not text:
            return ""

        text = self.normalize_unicode(text)
        text = self.clean_html(text)
        text = self._protect_emojis_manual(text)
        text = self.handle_urls(text)
        text = self.clean_symbols(text)
        text = self.collapse_repeats(text)
        text = self.clean_whitespace(text)
        text = self.normalize_case(text)
        text = self._restore_emojis(text)

        return text


# ---------------------- Interactive CLI ----------------------
def main():
    normalizer = TextNormalizer(
        unicode_form="NFC",
        max_char_repeat=2,
        max_punct_repeat=1,
        lowercase=True,
        remove_urls=False,
        normalize_urls=True,
        strip_html=True,
        preserve_emojis=True,
    )

    print("=" * 70)
    print("Text Normalizer — type your text and press Enter.")
    print("Type 'quit' or 'exit' (or press Ctrl+C) to stop.")
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

        try:
            result = normalizer.normalize(user_input)
            print("Normalized:", result)
        except Exception as e:
            print(f"[Error] {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()