from dataclasses import dataclass, field


@dataclass
class RawEntry:
    word: str
    html: str


@dataclass
class Example:
    english: str = ""
    persian: str = ""


@dataclass
class DictionaryEntry:
    word: str = ""
    ipa: str = ""
    part_of_speech: str = ""

    meanings: list[str] = field(default_factory=list)

    examples: list[Example] = field(default_factory=list)

    phrases: list[str] = field(default_factory=list)

    html: str = ""  

    audio: str = ""