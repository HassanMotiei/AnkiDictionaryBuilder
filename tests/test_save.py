from ankidict.importers.mdx import MDXImporter
from ankidict.parsers.aryanpur import AryanpurParser
from ankidict.repository.sqlite import SQLiteRepository

importer = MDXImporter("dictionaries/Aryanpur.mdx")

parser = AryanpurParser()

db = SQLiteRepository("dictionary.db")

raw = next(iter(importer))

entry = parser.parse(raw)

db.save(entry)

print("Saved:", entry.word)