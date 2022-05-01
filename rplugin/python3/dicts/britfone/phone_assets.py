"""
Language: en-GB
Static phonesets for the 'Britfone' dict
"""

import re

DIPTHONGS = set([
    "aɪ",
    "aʊ",
    "eɪ",
    "ɔɪ",
    "əʊ",
    "ɛə",
    "ɪə",
    "ʊə",
])

LONG_VOWELS = set([
    "iː",
    "uː",
    "ɑː",
    "ɔː",
    "ɜː",
])

SCHWA = "ə"

SHORT_VOWELS = set([
    "i",
    "ʊ",
    "æ",
    "ɐ",
    "ɒ",
    "ɛ",
    "ɪ",
])

AFFRICATES = set([
    "dʒ",
    "tʃ",
])

CONSONANTS = set([
    "p",
    "b",
    "t",
    "d",
    "k",
    "g",
    "f",
    "v",
    "s",
    "z",
    "ð",
    "θ",
    "ʃ",
    "ʒ",
    "m",
    "n",
    "ŋ",
    "j",
    "l",
    "w",
    "ɹ",
    "h",
    "ˈ", # RENAME AS STRESS
    "ˌ", # RENAME AS STRESS
])

PHONEMES = CONSONANTS | AFFRICATES | SHORT_VOWELS | LONG_VOWELS | DIPTHONGS | set(SCHWA)
VOWELS = SHORT_VOWELS | LONG_VOWELS | DIPTHONGS

PHONEMES_MATCH_STR = re.compile('('+'|'.join(sorted(list(PHONEMES), key=lambda x: len(x), reverse=True))+')')
HEAVY_SYLLABLE_MATCH_STR = f"({'|'.join(LONG_VOWELS)}|{'|'.join(DIPTHONGS)})"
SHORT_VOWELS_MATCH_STR = f"([{''.join(SHORT_VOWELS)}])"

CONS_OR_AFF = '(['+''.join(CONSONANTS)+'$]|'+'|'.join(AFFRICATES)+')'

# 2 chars
RE_DIPTHONGS = re.compile(f"({'|'.join(DIPTHONGS)})", flags=0)
RE_LONG_VOWELS = re.compile(f"({'|'.join(LONG_VOWELS)})", flags=0)
RE_AFFRICATES = re.compile(f"({'|'.join(AFFRICATES)})", flags=0)

RE_CONSONANTS = re.compile(f"[{''.join(CONSONANTS)}]", flags=0)

# e.g. "əʊ" or "tʃ"
FIRST_CHAR_BIPHONE = re.compile(
    f"({'|'.join([a[0] for a in AFFRICATES])}|" + \
    f"{'|'.join([l[0] for l in LONG_VOWELS])}|" + \
    f"{'|'.join([d[0] for d in DIPTHONGS])})",
    flags=0
)
