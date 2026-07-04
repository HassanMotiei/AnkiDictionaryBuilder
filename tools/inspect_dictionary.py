from pathlib import Path

from ankidict.importer import AryanpurImporter

OUTPUT = Path("output/html_samples")
OUTPUT.mkdir(parents=True, exist_ok=True)

importer = AryanpurImporter("dictionaries/Aryanpur.mdx")

for i, raw in enumerate(importer):

    filename = OUTPUT / f"{i:04d}_{raw.word}.html"

    filename.write_text(raw.html, encoding="utf-8")

    print(f"Saved {filename.name}")

    if i == 199:
        break

print("Done.")