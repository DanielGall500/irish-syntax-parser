from matcher import ComplementiserMatcher
from spacy.language import Language

class IrishComplementiserClassifier:
    def __init__(self, nlp: Language):
        self.matcher = ComplementiserMatcher()

    def __call__(self, lemmas: list[str]):
        matches = self.matcher(lemmas)
        return matches

    def match(self, sentence):
        return self.matcher(sentence)
