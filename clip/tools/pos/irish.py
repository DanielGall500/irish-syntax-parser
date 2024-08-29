from ...language.categories import UNIQUE_IRISH_NUMS, IRISH_RESUMPTIVE_PRONOUNS, IRISH_ADJECTIVES, IRISH_NOUNS, IRISH_DEFINITE_ARTICLES
from ..pos.pos_tagger import POSTagger 

"""
-- Irish POS Tagger --
This is a very basic lookup-based part-of-speech tagger (or verifier, moreso) for Irish.
It checks whether a word is a:
* Adjective
* Noun
* Resumptive Pronoun
Case is not relevant for these checks.
This should be expanded on to become a more comprehensive part-of-speech tagger in the future.
"""

class IrishPOSTagger(POSTagger):

    def __init__(self):
        resumptive_lookup = {str(res).lower() : True for res in IRISH_RESUMPTIVE_PRONOUNS}
        number_lookup = {str(num).lower() : True for num in UNIQUE_IRISH_NUMS}
        adj_lookup = {str(adj).lower() : True for adj in IRISH_ADJECTIVES}
        noun_lookup = {str(n).lower() : True for n in IRISH_NOUNS}
        definite_article_lookup = {str(n).lower() : True for n in IRISH_DEFINITE_ARTICLES}

        self.POS_lookup = {
            "ADJ": adj_lookup,
            "NOUN": noun_lookup,
            "RES": resumptive_lookup,
            "NUM": number_lookup,
            "DEF": definite_article_lookup
        }

    def is_POS(self, lemma: str, pos: str):
        return lemma in self.POS_lookup[pos]

    def is_adjective(self, lemma: str):
        return self.is_POS(lemma, "ADJ")

    def is_noun(self, lemma: str):
        return self.is_POS(lemma, "NOUN")

    def is_number(self, lemma: str):
        return self.is_POS(lemma, "NUM")

    def is_resumptive_pronoun(self, lemma: str):
        return self.is_POS(lemma, "RES")

    def is_definite_article(self, lemma: str):
        return self.is_POS(lemma, "DEF")