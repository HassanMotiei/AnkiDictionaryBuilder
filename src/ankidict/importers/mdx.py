from mdict_utils.base.readmdict import MDX

from ankidict.core.models import RawEntry



class MDXImporter:
    """Read entries from an MDX dictionary."""

    def __init__(self, filename: str):
        self.mdx = MDX(filename)

    def __iter__(self):
        for word, html in self.mdx.items():

            if isinstance(word, bytes):
                word = word.decode("utf-8", errors="replace")

            if isinstance(html, bytes):
                html = html.decode("utf-8", errors="replace")

            yield RawEntry(
                word=word,
                html=html,
            )