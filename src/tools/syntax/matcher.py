from language.categories import COMP_REALISATIONS, ALL_COMP_REALISATIONS
import numpy as np

class ComplementiserMatcher:

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
        return self.get_particle_outermost(ALL_COMP_REALISATIONS, lemmas)

    def get_go_particle(self, lemmas: list[str]) -> list:
        realisations = COMP_REALISATIONS['go']
        one_hot_encoding = self.get_particle(realisations, lemmas)
        return one_hot_encoding

    def get_a_particle(self, lemmas: list[str]) -> list:
        realisations = COMP_REALISATIONS['a']
        one_hot_encoding = self.get_particle(realisations, lemmas)
        return one_hot_encoding