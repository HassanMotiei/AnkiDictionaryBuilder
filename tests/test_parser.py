from ankidict.importers.mdx import MDXImporter
from ankidict.parsers.aryanpur import AryanpurParser

importer = MDXImporter("dictionaries/Aryanpur.mdx")
parser = AryanpurParser()

raw = next(iter(importer))

entries = parser.parse(raw)

for entry in entries:

    print(entry.word)
    print(entry.ipa)

    for ex in entry.examples:
        print("-" * 40)
        print(ex.english)
        print(ex.persian)

    print("POS:", entry.part_of_speech)
    print("=" * 50)