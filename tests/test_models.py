from src.models import DictionaryEntry, Example

entry = DictionaryEntry(
    word="ability",
    ipa="/əˈbɪləti/",
    part_of_speech="noun"
)

entry.meanings.append("توانایی")
entry.meanings.append("قابلیت")

entry.examples.append(
    Example(
        english="He has the ability to solve problems.",
        persian="او توانایی حل مسئله را دارد."
    )
)

print(entry)