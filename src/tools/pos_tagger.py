from abc import ABC, abstractmethod
import pandas as pd

IRISH_ADJ_PATH = "data/POS/focloir_adjectives.csv"
IRISH_NOUN_PATH = "data/POS/focloir_nouns.csv"

def get_lookup_from_focloir(path: str) -> dict:
    focloir_dataset = pd.read_csv(path)
    focloir_words = list(focloir_dataset['Item'])
    lookup = {w:True for w in focloir_words}
    return lookup

class POSTagger(ABC):
    @abstractmethod
    def is_POS(lemma: str, pos: str) -> bool:
        pass

    @abstractmethod
    def is_adjective(self, lemma: str) -> bool:
        pass

    @abstractmethod
    def is_noun(self, lemma: str) -> bool:
        pass

    @abstractmethod
    def is_POS(self, lemma: str, POS: str) -> bool:
        pass

class IrishPOSTagger(POSTagger):
    resumptive_pronouns = [
        "leat", "leis", "léi", "linn", "libh", "leo",
        "ort", "air", "uirthi", "orainn", "oraibh", "orthu",
        "agat", "aige", "aici", "againn", "agaibh", "acu",
        "duit", "dó", "di", "dúinn", "daoibh", "dóibh",
        "ionat", "ann", "inti", "ionainn", "ionaibh", "iontu"
    ]

    def __init__(self):
        adj_lookup = get_lookup_from_focloir(IRISH_ADJ_PATH)
        noun_lookup = get_lookup_from_focloir(IRISH_NOUN_PATH)

        resumptive_lookup = {res:True for res in self.resumptive_pronouns}

        self.POS_lookup = {
            "ADJ": adj_lookup,
            "NOUN": noun_lookup,
            "RES": resumptive_lookup
        }

    def is_POS(self, lemma: str, pos: str):
        return lemma in self.POS_lookup[pos]

    def is_adjective(self, lemma: str):
        return self.is_POS(lemma, "ADJ")

    def is_noun(self, lemma: str):
        return self.is_POS(lemma, "NOUN")

    def is_resumptive_pronoun(self, lemma: str):
        return self.is_POS(lemma, "RES")