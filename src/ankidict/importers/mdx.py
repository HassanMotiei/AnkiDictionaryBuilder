from mdict_utils.base.readmdict import MDX

from ankidict.core.models import RawEntry



class MDXImporter:
    """Read entries from an MDX dictionary."""

    def __init__(self, filename: str):
        self.mdx = MDX(filename)
        self._length = None
        
        def __len__(self):

            if self._length is None:

                self._length = sum(1 for _ in self.mdx.items())

            return self._length

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