from abc import ABC, abstractmethod

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
    def is_number(self, lemma: str) -> bool:
        pass
