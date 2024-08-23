from tools.syntax.complementisers import ComplementiserAnalyser
import json

comp_analyser = ComplementiserAnalyser()

class ClauseParser:
    def __init__(self):
        pass

    def __call__(self, lemmas: list[str]):
        all_clauses_analysed = []
        clauses = comp_analyser.get_comp_clauses(lemmas)
        clause_as_str = comp_analyser.get_comp_clauses_as_str(lemmas)
        for clause in clauses:
            c = clause["clause"]
            selected_comp = clause["selected_comp"]
            comp_preceded_by_noun = comp_analyser.clause_ends_in_noun(c)
            begins_with_adj = comp_analyser.clause_begins_with_adjective(c)
            begins_with_number = comp_analyser.clause_begins_with_number(c)
            resumptive_dict = comp_analyser.clause_contains_resumptive(c)
            resumptive_found = resumptive_dict["found"]
            resumptive_lemmas = resumptive_dict["lemma"]

            clause_info = {
                "clause": c,
                "selected_comp": selected_comp,
                "noun_final": comp_preceded_by_noun,
                "adj_initial": begins_with_adj,
                "number_initial": begins_with_number,
                "is_resumptive_found": resumptive_found,
                "resumptives": resumptive_lemmas
            }
            all_clauses_analysed.append(clause_info)
        return all_clauses_analysed

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

        lemmas = self.lemmatiser(sentence)
        clause_structure = self.clause_parser(lemmas)
        n_clauses = len(clause_structure)

        sentence_info["lemmas"] = lemmas
        sentence_info["clause_structure"] = clause_structure
        sentence_info["num_embedded_clauses"] = len(n_clauses)

def main():
    mccloskey_data_path = "data/mccloskey-complementiser-data.csv"
    mccloskey_data = pd.read_csv(mccloskey_data_path, header=0)
    irish_sentences = list(mccloskey_data['sentence_irish'])
    sentence_parser = SentenceParser()
    parsed_sentences = []

    for sentence in irish_sentences:
        parsed = sentence_parser(sentence)
        parsed_sentences.append(parsed)

    json_output = json.dumps(parsed_sentences)
    print(json_output)

if __name__ == "__main__":
    main()