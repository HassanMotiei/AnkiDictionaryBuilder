import re
from bs4 import BeautifulSoup

from ankidict.core.models import DictionaryEntry, Example, RawEntry


class AryanpurParser:

    # =========================================================
    # MAIN
    # =========================================================
    def parse(self, raw: RawEntry):

        soup = BeautifulSoup(raw.html, "lxml")

        entry = DictionaryEntry()

        entry.word = raw.word
        entry.html = raw.html

        entry.ipa = self.extract_ipa(soup)
        entry.meanings = self.extract_meanings(soup)
        entry.examples = self.extract_examples(soup)
        entry.part_of_speech = self.extract_part_of_speech(soup)

        return entry

    # =========================================================
    # NOISE FILTER
    # =========================================================
    def is_noise(self, text: str) -> bool:

        text = text.strip()

        if not text:
            return True

        if text.startswith("-"):
            return False  # important: meanings start with "-"

        if len(text) <= 2:
            return True

        # fragment words like vt., adj., etc handled elsewhere
        if re.fullmatch(r"[a-zA-Z]{1,3}\.?", text):
            return True

        return False

    # =========================================================
    # POS DETECTION
    # =========================================================
    def is_pos(self, text: str) -> bool:

        return bool(re.fullmatch(
            r"(noun|verb|adj|adjective|adv|adverb|prep|article|interj|vt|vi)\.?",
            text.lower()
        ))

    # =========================================================
    # IPA
    # =========================================================
    def extract_ipa(self, soup):

        text = soup.get_text(" ", strip=True)

        match = re.search(r"/(.*?)/", text)

        return f"/{match.group(1).strip()}/" if match else ""

    # =========================================================
    # MEANINGS
    # =========================================================
    def extract_meanings(self, soup):

        meanings = []

        for p in soup.find_all("p"):

            text = p.get_text(" ", strip=True)

            if self.is_pos(text):
                continue

            if "●" in text:
                text = text.replace("●", "").strip()

            elif text.startswith("-"):
                text = text[1:].strip()

            else:
                continue

            if self.is_noise(text):
                continue

            meanings.append(text)

        return meanings


    # =========================================================
    # STRUCTURE MEANINGS
    # (Disabled for now)
    # =========================================================
    def structure_meanings(self, meanings):
        """
        Reserved for future semantic parser.

        Current parser always returns:
            list[str]

        Never:
            list[list[str]]
        """
        return meanings

    # =========================================================
    # STRUCTURE MEANINGS INTO SENSES
    # =========================================================
    def structure_meanings(self, meanings):

        if not meanings:
            return []

        grouped = []
        current = []

        for m in meanings:

            # sense breaker heuristics
            if self.is_sense_break(m):

                if current:
                    grouped.append(current)
                    current = []

                current.append(m)
                continue

            current.append(m)

        if current:
            grouped.append(current)

        # flatten single group
        return grouped if len(grouped) > 1 else grouped[0] if grouped else []

    # =========================================================
    # SENSE BREAK DETECTOR
    # =========================================================
    def is_sense_break(self, text: str) -> bool:

        return any(x in text for x in [
            "موسیقی",
            "رجوع",
            "گروه خونی",
            "زیست",
            "کامپیوتر",
        ])

    # =========================================================
    # EXAMPLES
    # =========================================================
    def extract_examples(self, soup):

        paragraphs = []

        for p in soup.find_all("p"):

            text = p.get_text(" ", strip=True)
            if not text:
                continue

            paragraphs.append({
                "text": text,
                "dir": (p.get("dir") or "").lower()
            })

        examples = []

        i = 0

        while i < len(paragraphs) - 1:

            cur = paragraphs[i]
            nxt = paragraphs[i + 1]

            if cur["dir"] == "ltr" and nxt["dir"] == "rtl":

                if self.is_valid_example(cur["text"]):

                    examples.append(
                        Example(
                            english=cur["text"],
                            persian=nxt["text"]
                        )
                    )

                i += 2
            else:
                i += 1

        return examples

    # =========================================================
    # VALID EXAMPLE
    # =========================================================
    def is_valid_example(self, text: str) -> bool:

        return (
            bool(re.search(r"[a-zA-Z]", text))
            and len(text.split()) >= 2
        )

    # =========================================================
    # POS EXTRACTION
    # =========================================================
    def extract_part_of_speech(self, soup):

        for tag in soup.find_all("font", {"color": "#007000"}):

            text = tag.get_text(" ", strip=True)

            m = re.match(r"([A-Za-z.]+)", text)

            if m:
                return m.group(1)

        return ""