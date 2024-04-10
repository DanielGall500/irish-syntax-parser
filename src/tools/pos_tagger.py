from tools.lemmatiser import IrishLemmatiser
import pandas as pd
from abc import ABC, abstractmethod

class POSTagger(ABC):
    @abstractmethod
    def is_adjective(self, lemma: str):
        pass

    @abstractmethod
    def is_noun(self, lemma: str):
        pass

    @abstractmethod
    def is_POS(self, lemma: str, POS: str):
        pass

# this is too specific to the format of the CSV file
class IrishPOSTagger(POSTagger):
    def __init__(self):
        self.adj_path = "data/POS/focloir_adjectives.csv"
        self.noun_path = "data/POS/focloir_nouns.csv"

        adjectives = pd.read_csv(self.adj_path)
        adjs_as_list = list(adjectives['Item'])
        adj_lookup = {adj:True for adj in adjs_as_list}

        nouns = pd.read_csv(self.noun_path)
        nouns_as_list = list(nouns['Item'])
        noun_lookup = {noun:True for noun in nouns_as_list}

        resumptive_pronouns = ['liom']
        resumptive_lookup = {res:True for res in resumptive_pronouns}

        self.POS_lookup = {
            "ADJ": adj_lookup,
            "NOUN": noun_lookup,
            "RES": resumptive_pronouns
        }

    def is_POS(self, lemma: str, pos: str):
        return lemma in self.POS_lookup[pos]

    def is_adjective(self, lemma: str):
        return self.is_POS(lemma, "ADJ")

    def is_noun(self, lemma: str):
        return self.is_POS(lemma, "NOUN")

    def is_resumptive_pronoun(self, lemma: str):
        return self.is_POS(lemma, "RES")