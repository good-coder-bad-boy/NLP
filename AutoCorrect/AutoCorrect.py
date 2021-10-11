"""
Spelling Corrector in Python 3; see http://norvig.com/spell-correct.html

Copyright (c) 2007-2016 Peter Norvig
MIT license: www.opensource.org/licenses/mit-license.php

Modified by GoodCoderBBoy 2021
"""

from collections import Counter
from re import findall


with open("AutoCorrect/big.txt") as f:
    WORDS = Counter(findall("\\w+", f.read().lower()))

MAX = WORDS.most_common(1)[0][1] # maximum count of any word

class AutoCorrect:
    def Correct(self, word: str, options: Counter=WORDS) -> str: 
        """
        Most probable spelling correction for word.
        """

        return self.Candidates(word, options=options)[0]

    def Candidates(self, word: str, maxitems: int=100, options: Counter=WORDS) -> list[str]:
        """
        Generate possible spelling corrections for word in order of likelyhood.
        """

        if word == "":
            return list(dict(options.most_common(maxitems)).keys())

        res: list = (
            [
                w for w in [word.lower()] if w in options.keys()
            ] + sorted(
                list(
                    set(
                        [
                            w for w in self.__edits1(word.lower()) if w in options.keys()
                        ] + [
                            w for w in self.__edits2(word.lower()) if w in options.keys()
                        ]
                    )
                ),
                key=options.get,
                reverse=True
            ) + [
                word.lower()
            ]
        )

        return [
            (
                w * (word == "")
            ) or (
                w.upper() * (word.isupper() and len(word) > 1)
            ) or (
                w.capitalize() * word[0].isupper()
            ) or (
                w
            ) for w in res[:min(maxitems, len(res))]
        ]

    def __edits1(self, word: str) -> set[str]:
        """
        All edits that are one edit away from word.
        """

        letters = "abcdefghijklmnopqrstuvwxyz"

        original   = [wd                      for wd in [word]]
        splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
        deletes    = [L + R[1:]               for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
        inserts    = [L + c + R               for L, R in splits for c in letters]
        
        return set(
            original + deletes + transposes + replaces + inserts
        )

    def __edits2(self, word: str) -> set[str]: 
        """
        All edits that are two edits away from word.
        """

        return set(
            e2 for e1 in self.__edits1(word) for e2 in self.__edits1(e1)
        )

