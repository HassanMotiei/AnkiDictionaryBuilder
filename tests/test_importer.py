from ankidict.importer import AryanpurImporter

imp = AryanpurImporter("dictionaries/Aryanpur.mdx")

entry = next(iter(imp))

print(entry.word)
print(entry.html[:300])