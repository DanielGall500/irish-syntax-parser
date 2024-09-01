from .complementisers import ComplementiserAnalyser
from ...preprocessing.string_manipulation import remove_eos_characters
from ..morphology.lemmatiser import IrishLemmatiser
import json

class ParsedSentence:
    def __init__(self, sentence: dict):
        self.sentence = sentence

    def as_dict(self):
        return self.sentence

    def get_full_sentence(self):
        return self.sentence["full"]

    def get_main_comp(self) -> str | None:
        return self[0]["selected_comp"]

    def get_comp(self, index: int) -> str | None:
        if index < self.get_num_clauses():
            return self[index]["selected_comp"]

    def get_num_clauses(self):
        return self.sentence["num_clauses"]

    def set_comp(self, index: int, c: str) -> bool:
        if index < self.get_num_clauses():
            self[index]["selected_comp"] = c
            return True
        return False

    def __iter__(self):
        self.curr_clause = self.sentence["clause_structure"]
        return self
    
    def __next__(self):
        if self.curr_clause is None:
            raise StopIteration

        clause_to_return = self.curr_clause
        self.curr_clause = self.curr_clause.get("embedded_clause", None)
        
        return clause_to_return

    def __getitem__(self, index):
        for i, clause in enumerate(self):
            if i == index:
                return clause
        raise KeyError

class IrishClauseParser:
    def __init__(self):
        self.clause_parser = ClauseParser()
        self.lemmatiser = IrishLemmatiser()

    def __call__(self, sentence: str):
        parsed_sentence = self.parse_to_dict(sentence)
        return ParsedSentence(parsed_sentence)

    def parse_to_dict(self, sentence: str):
        sentence_info = {
            "full": sentence,
            "lemmas": None,
            "clause_structure": None,
            "num_clauses": None
        }

        # perform preprocessing on the string and convert it to a list of lemmas
        without_special_characters = remove_eos_characters(sentence)
        lemmas = self.lemmatiser(without_special_characters)
        n_clauses, clause_structure = self.clause_parser(lemmas)

        sentence_info["lemmas"] = lemmas
        sentence_info["clause_structure"] = clause_structure
        sentence_info["num_clauses"] = n_clauses
        return sentence_info

    def parse_to(self, sentences: list[str], path: str):
        parsed_sentences = []
        for s in sentences:
            parsed_s = self.parse_to_dict(s)
            parsed_sentences.append(parsed_s)

        with open(path, 'w', encoding='utf-8') as file:
            json.dump(parsed_sentences, file, indent=4, ensure_ascii=False)
        
    def read_from(self, path: str) -> list[dict] | None:
        try:
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
                if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                    return [ParsedSentence(s) for s in data]
                else:
                    raise ValueError("The JSON data is not a list of dictionaries.")
        except FileNotFoundError:
            print(f"Error: The file {path} was not found.")
        except json.JSONDecodeError:
            print(f"Error: The file {path} does not contain valid JSON.")
        except ValueError as ve:
            print(f"Error: {ve}")
        return None

class ClauseParser:
    def __init__(self):
        self.comp_analyser = ComplementiserAnalyser()

    def __call__(self, lemmas: list[str]):
        return self.parse(lemmas)

    def parse(self, lemmas: str):
        clauses = self.comp_analyser.get_comp_clauses(lemmas)
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
        comp_preceded_by_noun = self.comp_analyser.clause_ends_in_noun(lemmas)
        begins_with_adj = self.comp_analyser.clause_begins_with_adjective(lemmas)
        begins_with_number = self.comp_analyser.clause_begins_with_number(lemmas)
        resumptive_dict = self.comp_analyser.clause_contains_resumptive(lemmas)
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

