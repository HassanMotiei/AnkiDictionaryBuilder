from ankidict.importers.mdx import MDXImporter
from ankidict.parsers.aryanpur import AryanpurParser
from ankidict.core.engine import DictionaryEngine


engine = DictionaryEngine()

engine.load(
    importer=MDXImporter("dictionaries/Aryanpur.mdx"),
    parser=AryanpurParser()
)

for i, entry in enumerate(engine.process_all()):

    print(entry.word)
    print(entry.ipa)

    for m in entry.meanings:
        print("-", m)

    print("=" * 40)

    if i == 2:
        break