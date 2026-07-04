from ankidict.importers.mdx import MDXImporter
from ankidict.parsers.aryanpur import AryanpurParser
from ankidict.repository.sqlite import SQLiteRepository
from ankidict.core.engine import DictionaryEngine

engine = DictionaryEngine()

engine.load(
    importer=MDXImporter("dictionaries/Aryanpur.mdx"),
    parser=AryanpurParser(),
)

db = SQLiteRepository("dictionary.db")

engine.build_database(db)