from tools.pos.irish import IrishPOSTagger
from tools.syntax.matcher import ComplementiserMatcher

"""
-- Syntax Manager --
This is a class which checks the syntax of Irish expressions.
It uses string manipulation and the part-of-speech tagger in order to
check whether an individual sentence follows a certain syntactic pattern.

It can check whether a given complementiser (go, aN, aR):
* Is directly preceded by a noun.
* Is directly followed by an adjective.
* Contains a potential resumptive pronoun with in the embedded clause.
"""
class ComplementiserAnalyser:
    tagger = IrishPOSTagger()
    matcher = ComplementiserMatcher()

    def __init__(self):
        pass 

    # A cyclic function to iterate through each clause of a sentence.
    # Cyclicity concerns the notion of iterating over nested layers
    # in a hierarchical structure.
    # This implementation uses recursion.
    def get_comp_clauses(self, lemmas: list) -> list:
        return self._get_comp_clauses_recursive(lemmas, [])

    def _get_comp_clauses_recursive(self, lemmas: list, clauses: list) -> list:
        comp_index = self.matcher.get_complementiser_outermost(lemmas)
        if comp_index != -1:
            main_clause = self._get_main_clause(lemmas, comp_index)
            embedded_clause = self._get_embedded_clause(lemmas, comp_index)
            comp = lemmas[comp_index]
            clauses.append({
                "clause": main_clause,
                "selected_comp": comp
            })
            return self._get_comp_clauses_recursive(embedded_clause, clauses)
        else:
            clauses.append({
                "clause": lemmas,
                "selected_comp": None
            })
            return clauses

    def get_comp_clauses_as_str(self, lemmas: list) -> list:
        clause_info = self.get_comp_clauses(lemmas)
        clauses = [c['clause'] for c in clause_info]

        full_str = ""

        for i, c in enumerate(clause_info):
            clause = " ".join(c['clause'])
            selected_comp = c['selected_comp']
            selected_comp = selected_comp if selected_comp else ""
            print("Clause", clause)
            print("Selected,", selected_comp)
            full_str = full_str + " [ " + clause + " " + selected_comp
        full_str = full_str + " ]"*len(clause_info)
        return full_str


    def is_followed_by_number(self, lemmas: list, comp_index: int) -> bool:
        embedded_clause = self._get_embedded_clause(lemmas, comp_index)
        embedded_clause_exists = len(embedded_clause) > 0

        if embedded_clause_exists:
            # take the very first lemma in the embedded clause
            first_lemma = embedded_clause[0]
            return self.tagger.is_number(first_lemma)
        return False

    def is_preceded_by_noun(self, lemmas: list, comp_index: int) -> bool:
        # store everything up to the given complementiser
        # the complementiser is indicated by the index

        main_clause = self._get_main_clause(lemmas, comp_index)
        main_clause_exists = len(main_clause) > 0

        # if there is a main clause to the left of the complementiser
        if main_clause_exists:
            # take the final lemma of the main clause
            final_lemma = main_clause[-1]

            # check whether that lemma is a noun
            return self.tagger.is_noun(final_lemma)
        return False

    def is_followed_by_adjective(self, lemmas: list, comp_index: int):
        # does not take into account when the adjective
        # looks like a noun.
        # right_of_comp = row['Right'].lower()

        # store everything in the embedded clause
        embedded_clause = self._get_embedded_clause(lemmas, comp_index)
        embedded_clause_exists = len(embedded_clause) > 0

        if embedded_clause_exists:
            # take the very first lemma in the embedded clause
            first_lemma = embedded_clause[0]

            # check whether the first lemma in the embedded clause
            # is an adjective in Irish
            return self.tagger.is_adjective(first_lemma)
        return False

    def contains_resumptive(self, lemmas: list, comp_index: int) -> list:
        resumptive_object = {
            "found": False,
            "lemma": None
        }

        # store everything in the embedded clause
        embedded_clause = self._get_embedded_clause(lemmas, comp_index)
        embedded_clause_exists = len(embedded_clause) > 0

        if embedded_clause_exists:
            # check every lemma in the embedded clause
            # and output True is a resumptive pronoun
            # is found
            for lemma in embedded_clause:
                if self.tagger.is_resumptive_pronoun(lemma):
                    resumptive_object["found"] = True
                    resumptive_object["lemma"] = lemma
                    break
        return resumptive_object

    # complementiser is excluded in both cases
    def _get_main_clause(self, lemmas: list, comp_index: int) -> list:
        return lemmas[:comp_index]

    def _get_embedded_clause(self, lemmas: list, comp_index: int) -> list:
        return lemmas[comp_index+1:]

