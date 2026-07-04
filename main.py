from readmdict import MDX

mdx = MDX("dictionaries/aryanpour.mdx")

print("Loading dictionary...")

count = 0

for word, definition in mdx.items():
    try:
        word = word.decode("utf-8")
    except:
        word = word.decode("utf-8", errors="ignore")

    try:
        definition = definition.decode("utf-8")
    except:
        definition = definition.decode("utf-8", errors="ignore")

    print(word)
    print("=" * 50)
    print(definition[:1000])   # فقط 1000 کاراکتر اول
    break