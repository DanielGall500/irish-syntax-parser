from tools.syntax.complementisers import ComplementiserAnalyser
from preprocessing.string_manipulation import remove_eos_characters
import pandas as pd
import json

comp_analyser = ComplementiserAnalyser()

class ClauseParser:
    def __init__(self):
        pass

    def __call__(self, lemmas: list[str]):
        return self.parse(lemmas)

    def parse(self, lemmas: str):
        clauses = comp_analyser.get_comp_clauses(lemmas)
        starting_clause = 0
        n_clauses = len(clauses)
        parsed_clauses = self._parse_recursive(clauses, n_clauses, starting_clause)
        return n_clauses, parsed_clauses

    def _parse_recursive(self, clauses: list[list[str]], n_clauses: int, curr_clause: int):
        clause_info = {}

        # get all the information needed for encoding the clause
        c = clauses[curr_clause]
        lemmas = c["clause"]
        selected_comp = c["selected_comp"]
        comp_preceded_by_noun = comp_analyser.clause_ends_in_noun(lemmas)
        begins_with_adj = comp_analyser.clause_begins_with_adjective(lemmas)
        begins_with_number = comp_analyser.clause_begins_with_number(lemmas)
        resumptive_dict = comp_analyser.clause_contains_resumptive(lemmas)
        resumptive_found = resumptive_dict["found"]
        resumptive_lemmas = resumptive_dict["lemma"]

        # if there are more embedded clauses, continue
        if curr_clause+1 < n_clauses:
            embedded_clause = self._parse_recursive(clauses, n_clauses, curr_clause+1)
        # otherwise, break the recursive function
        else:
            embedded_clause = None

        # form the embedded dictionary object
        clause_info = {
            "clause": lemmas,
            "selected_comp": selected_comp,
            "noun_final": comp_preceded_by_noun,
            "adj_initial": begins_with_adj,
            "number_initial": begins_with_number,
            "is_resumptive_found": resumptive_found,
            "resumptives": resumptive_lemmas,
            "embedded_clause": embedded_clause
        }
        return clause_info


class SentenceParser:
    def __init__(self):
        self.clause_parser = ClauseParser()

        # remove this:
        from tools.morphology.lemmatiser import IrishLemmatiser
        self.lemmatiser = IrishLemmatiser()

    def __call__(self, sentence: str):
        sentence_info = {
            "full": sentence,
            "lemmas": None,
            "clause_structure": None,
            "num_embedded_clauses": None
        }

        # perform preprocessing on the string and convert it to a list of lemmas
        without_special_characters = remove_eos_characters(sentence)
        lemmas = self.lemmatiser(without_special_characters)
        n_clauses, clause_structure = self.clause_parser(lemmas)

        sentence_info["lemmas"] = lemmas
        sentence_info["clause_structure"] = clause_structure
        sentence_info["num_clauses"] = n_clauses
        return sentence_info

def main():
    mccloskey_data_path = "data/mccloskey-complementiser-data.csv"
    mccloskey_data = pd.read_csv(mccloskey_data_path, header=0)
    irish_sentences = list(mccloskey_data['sentence_irish'])
    english_translations = list(mccloskey_data['sentence_english'])
    sentence_parser = SentenceParser()
    parsed_sentences = []

    for sentence in irish_sentences:
        parsed = sentence_parser(sentence)
        parsed_sentences.append(parsed)

    for i, ps in enumerate(parsed_sentences):
        ps["english_translation"] = english_translations[i]

    with open('data/clause_info.json', 'w', encoding='utf-8') as file:
        json.dump(parsed_sentences, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()