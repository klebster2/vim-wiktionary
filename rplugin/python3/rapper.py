import pynvim

import sys
import json
import os

from collections.abc import Iterable
from collections import defaultdict

from typing import Iterable, Tuple

import re

from dicts.britfone.britfone_dict import LoadBritfoneDict
from dicts.beep.beep_dict import LoadBeepDict
from dicts.britfone.phone_assets import (
        HEAVY_SYLLABLE_MATCH_STR,
        SHORT_VOWELS_MATCH_STR,
)

class Ui(object):
    """
    grab data from the UI at the current point in time (assume static)
    """

    @classmethod
    def _get_word(self, line, col_n):
        """
        gets the current word under the cursor in the nvim session
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

@pynvim.plugin
class VimForPoetsPlugin(object):
    """
    Some methods were inspired by Allison Parrish's work in the library pronouncingpy
    see: https://github.com/aparrish/pronouncingpy

    In essence, we want to expose literary devices in this plugin that are
    commonly used by poets, lyricists and writers and can be implemented by modern nlp.

    The idea is to start with english (GB) and build out languages from there.

    The fact is that today good models are not in short supply.

    This could include but are not limited to
    rhyming
    punning
    consonance AKA assonance
    allegory
    anagrams
    palindromes
    merism
    hyperbaton
    rhetorical questions
    catachresis
    prolepsis
    anaphora
    congeries
    hyperbole
    etc.

    Additionally, models such as word2vec fasttext, gpt-2, and gpt-3 enable
    fine tuning large models that have been pretrained on massive amounts of data
    for almost any task.

    E.g.
    Peter piper picked a pack of pickled peppers
    makes use of /p/ to construct an assonant device

    We can additionally find rhymes using regular expressions
    """
    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.command('LoadBritfoneDict')
    def _load_britfone_dict(self):
        """
        loads the britfone british english pphonemic dictionary
        """
        self._phonedict, self._phonedict_rev = LoadBritfoneDict().load()

    @pynvim.command('LoadBeepDict')
    def _load_beep_dict(self):
        """
        loads the beep british english phonemic dictionary
        """
        self._phonedict, self._phonedict_rev = LoadBeepDict().load()

    def _phones_for_word(self, word):
        return self._phonedict.get(word)

    def _stresses_for_word(self, word):
        raise NotImplementedError

    def _rhyming_part(self, query_phones:list) -> list:
        rhyming_part_matches = []
        for phones in query_phones:
            _rhyming_part_heavy_match = re.match(rf".*\b[ˌˈ]?({HEAVY_SYLLABLE_MATCH_STR}\b.*)$", phones)
            _rhyming_part_light_match = re.match(rf".*\b[ˌˈ]?({SHORT_VOWELS_MATCH_STR}\b.*)$", phones)
            if _rhyming_part_heavy_match:
                rhyming_part_matches.append(_rhyming_part_heavy_match.group(1))
            if _rhyming_part_light_match:
                rhyming_part_matches.append(_rhyming_part_light_match.group(1))

        return rhyming_part_matches

    @pynvim.command('RhymeWord', sync=True)
    def rhyme_word(self):
        rhymes=[]
        col_n = self.nvim.eval("col('.')")
        line = self.nvim.eval("getline('.')")
        word_start, query_word = Ui._get_word(line, col_n)
        query_word = query_word.upper()
        query_phones = self._phonedict_rev.get(query_word)
        if query_phones:
            rhyming_parts = self._rhyming_part(query_phones)
            for phones, words in self._phonedict.items():
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

    def _assonance(self, phones):
        """
        Assonance AKA Consonance, is similar to alliteration.
        We can implement this using cosine similarity, or prime numbers

        https://en.wikipedia.org/wiki/Assonance
        https://en.wikipedia.org/wiki/Literary_consonance
        """
        raise NotImplementedError

    def _anagrams(self, word):
        """
        Abstract away to a simple wordlist
        """
        raise NotImplementedError
