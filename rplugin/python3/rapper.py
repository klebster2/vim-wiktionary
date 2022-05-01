import pynvim

import sys
import json
import os

from collections.abc import Iterable
from collections import defaultdict

from typing import Iterable, Tuple

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
    "ˈ",
    "ˌ",
])

PHONEMES = CONSONANTS | AFFRICATES | SHORT_VOWELS | LONG_VOWELS | DIPTHONGS | set(SCHWA)

RE_PHONEMES = re.compile('('+'|'.join(sorted(list(PHONEMES), key=lambda x: len(x), reverse=True))+')')

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

RE_HEAVY_SYLLABLE = f"({'|'.join(LONG_VOWELS)}|{'|'.join(DIPTHONGS)})"
RE_SHORT_VOWELS = f"([{''.join(SHORT_VOWELS)}])"

VOWELS = SHORT_VOWELS | LONG_VOWELS | DIPTHONGS

CONS_OR_AFF = '(['+''.join(CONSONANTS)+'$]|'+'|'.join(AFFRICATES)+')'

class BaseDict:
    def __init__(self, path_to_dict):
        pass
#    def __init__(self):
#        # download beepdict
#        import tarfile
#        
#        # open file
#        file = tarfile.open('gfg.tar.gz')
#        
#        # extracting file
#        file.extractall('./Destination_FolderName')
#        
#        file.close()

class BeepDict(BaseDict):
    pass
# TODO - add to britfonedict


class BritfoneDict(BaseDict):
    pass

@pynvim.plugin
class RapperPlugin(object):
    """
    Some methods here are inspired by Allison Parrish's work here:
    e.g. https://github.com/aparrish/pronouncingpy
    """
    def __init__(self, nvim):
        self.nvim = nvim

    @classmethod
    def _get_word(self, line, col_n):
        """
        gets word under current
        """
        globally_nearest_left = 0
        globally_nearest_right  = len(line)

        for m in re.finditer("^|\s+|$", line):
            # save spans between current column and boundaries
            if col_n - m.span()[1] < globally_nearest_left and (col_n - m.span()[1]) > 0:
                globally_nearest_left = m.span()[1]
            if m.span()[0] - col_n < globally_nearest_right and (m.span()[0] - col_n) > 0:
                globally_nearest_right = m.span()[0]

        word = line[globally_nearest_left:globally_nearest_right]
        return globally_nearest_left, word

    @pynvim.command('LoadBritfoneDict', sync=False)
    def _load_britfone_dict(self, path_to_dict):
        SEP = "\s+"
        with open(path_to_dict, 'r') as f:
            self._britfone = defaultdict(list)
            self._britfone_rev = defaultdict(list)
            for idx, line in enumerate(f.readlines()):
                if line[0] == "#":
                    continue
                try:
                    word, phones = re.match(r'(\S+){SEP}(.*)',line).groups()
                except:
                    raise ValueError("Unable to parse idx:{idx} line:{line}")

                self._britfone[phones].append(word)
                self._britfone_rev[word].append(phones)

    @pynvim.command('LoadBeepDict', sync=False)
    def _load_beep_dict(self, path_to_dict):
        SEP = ",\s+"
        with open(path_to_dict, 'r') as f:
            self._britfone = defaultdict(list)
            self._britfone_rev = defaultdict(list)
            for idx, line in enumerate(f.readlines()):
                if line[0] == "#":
                    continue
                try:
                    word, phones = re.match(rf'(\S+){SEP}(.*)',line).groups()
                except:
                    raise ValueError("Unable to parse idx:{idx} line:{line}")

                self._britfone[phones].append(word)
                self._britfone_rev[word].append(phones)

    def _phones_for_word(self, word):
        return self._britfone.get(word)

    def _stresses_for_word(self, word):
        raise NotImplementedError("Not Implemented")

    def _rhyming_part(self, query_phones:list) -> list:
        rhyming_part_matches = []
        for phones in query_phones:
            _rhyming_part_heavy_match = re.match(rf".*\b[ˌˈ]?({RE_HEAVY_SYLLABLE}\b.*)$", phones)
            _rhyming_part_light_match = re.match(rf".*\b[ˌˈ]?({RE_SHORT_VOWELS}\b.*)$", phones)
            if _rhyming_part_heavy_match:
                rhyming_part_matches.append(_rhyming_part_heavy_match.group(1))
            if _rhyming_part_light_match:
                rhyming_part_matches.append(_rhyming_part_light_match.group(1))

        return rhyming_part_matches

    def _assonance(self, phones):
        """
        Assonance AKA Consonance, which is similar to alliteration.
        We can implement this using cosine similarity

        https://en.wikipedia.org/wiki/Assonance
        https://en.wikipedia.org/wiki/Literary_consonance
        """
        pass

    def _anagrams(self, word):
        """
        Abstract away to a simple wordlist
        """
        pass

    @pynvim.command('RhymeWord', sync=True)
    def rhyme_word(self):
        rhymes=[]
        col_n = self.nvim.eval("col('.')")
        line = self.nvim.eval("getline('.')")
        word_start, query_word = self._get_word(line, col_n).lower()
        query_phones = self._britfone_rev.get(query_word)
        if query_phones:
            rhyming_parts = self._rhyming_part(query_phones)
            for phones, words in self._britfone.items():
                for rhyming_part in rhyming_parts:
                    if re.match(f'.*{rhyming_part}$', phones):
                        for word in words:
                            rhymes.append(
                                {
                                    'icase': 1,
                                    "word": word,
                                    "menu": phones,
                                }
                            )
        rhymes.insert(
            0,
            {
                'icase': 1,
                "word": query_word,
                "menu": f"NO RHYMING WORDS FOUND FOR {query_word}" if not rhymes else '|'.join(query_phones),
            }
        )

        return self.nvim.funcs.complete(word_start, rhymes)
