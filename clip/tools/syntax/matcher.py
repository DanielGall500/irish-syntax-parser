from ...language.categories import COMP_REALISATIONS, ALL_COMP_REALISATIONS
from ..pos.irish import IrishPOSTagger
import numpy as np

class ComplementiserMatcher:
    pos_tagger = IrishPOSTagger()

    def __call__(self, lemmas: list[str]) -> np.array:
        go_particle = self.get_go_particle(lemmas)
        a_particle = self.get_a_particle(lemmas)
        matrix = np.vstack((go_particle, a_particle))
        return matrix
    
    def get_sum_of_occurrences(self, lemmas: list[list[str]]) -> np.array:
        matrices = []
        for l in lemmas:
            matrix = self.__call__(l)
            matrices.append(matrix)

        complementiser_sums = np.array([0,0])
        for m in matrices:
            sums = np.sum(m, axis=1)
            complementiser_sums = np.add(complementiser_sums, sums)
        return complementiser_sums

    def get_particle(self, realisations: list[str], lemmas: list[str]) -> list[int]:
        n = len(lemmas)
        one_hot_encoding = np.zeros(n)
        for i,token in enumerate(lemmas):
            if token in realisations:
                one_hot_encoding[i] = 1
        return one_hot_encoding

    def get_particle_outermost(self, realisations: list[str], lemmas: list[str]) -> int:
        for i, token in enumerate(lemmas):
            if token in realisations:
                return i
        return -1

    def get_complementiser_outermost(self, lemmas: list[str]) -> int:
        comp_index = self.get_particle_outermost(ALL_COMP_REALISATIONS, lemmas)

        # no potential complementisers found
        if comp_index == -1:
            return comp_index

        # account for the possibility of the complementiser
        # being a preposition, as they can have the same
        # surface forms
        if self.compcheck_is_prep(lemmas, comp_index):
            return -1
        
        return comp_index

    def compcheck_is_prep(self, lemmas: list[str], comp_index: int):
        comp_realisation = lemmas[comp_index]
        highest_lemma_index = len(lemmas)-1

        # if there is a word after the comp
        if comp_index+1 < highest_lemma_index:
            following_word = lemmas[comp_index+1]

            # account for prepositional phrase "go dtí"
            if comp_realisation == "go" and following_word == "dtí":
                return True
            # account for prepositional phrases like "ar an..." (on the)
            # Irish is verb-initial, so a noun-initial phrase indicates a preposition
            NP_initial = self.pos_tagger.is_definite_article(following_word) or self.pos_tagger.is_noun(following_word)
            if comp_realisation == "ar" and NP_initial:
                return True
            
            # check if preposition for a number (remember verb-initial)
            if comp_realisation == "go" and self.pos_tagger.is_number(following_word):
                return True

            if comp_realisation == "go" and self.pos_tagger.is_adjective(following_word):
                return True
        return False

    def get_go_particle(self, lemmas: list[str]) -> list:
        realisations = COMP_REALISATIONS['go']
        one_hot_encoding = self.get_particle(realisations, lemmas)
        return one_hot_encoding

    def get_a_particle(self, lemmas: list[str]) -> list:
        realisations = COMP_REALISATIONS['a']
        one_hot_encoding = self.get_particle(realisations, lemmas)
        return one_hot_encoding