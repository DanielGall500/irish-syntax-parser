from .tools.syntax.parser import IrishClauseParser, ParsedSentence
import pandas as pd

GO_MODERN_RESUMPTIVE_TAG = "goN"
A_RESUMPTIVE_TAG = "aN"
A_GAP_TAG = "aL"

class McCloskeyParser:
    def __init__(self):
        self.clause_parser = IrishClauseParser()

    def __call__(self, sentence: str):
        parsed_sentence = self.clause_parser(sentence)
        mccloskey_parsed = self.parse(parsed_sentence)
        return mccloskey_parsed

    def parse(self, ps: ParsedSentence):
        mccloskey_parsed_s = ps
        n_clauses = ps.get_num_clauses()

        if n_clauses > 1:
            selected_comps = []
            XP_preceding_comps = []
            resumptives = []
            for i,clause in enumerate(ps):
                category = "DP" if clause["noun_final"] else "XP"
                mccloskey_parsed_s[i]["preceding_category"] = category
                resumptives.append(clause["is_resumptive_found"])
                del mccloskey_parsed_s[i]["noun_final"]
                del mccloskey_parsed_s[i]["adj_initial"]
                del mccloskey_parsed_s[i]["number_initial"]

                comp = clause["selected_comp"]

                # REPLACE WITH LANGUAGE DATA
                if comp:
                    if comp in ["go", "gur", "gurbh", "gurb"]:
                        comp = "go"
                    elif comp in ["ar"]:
                        comp = "a"
                    mccloskey_parsed_s.set_comp(i, comp)

                    XP_preceding_comps.append(category)
                    selected_comps.append(comp)

            # a number of checks on the clause structure
            is_resumptive_in_final_clause = resumptives[-1]
            is_go_in_embedded_clauses = all(c == "go" for c in selected_comps[1:])
            is_gap_structure = all(c == "a" for c in selected_comps)
            is_main_clause_a = mccloskey_parsed_s.get_main_comp() == "a"
            is_main_clause_go = mccloskey_parsed_s.get_main_comp() == "go"

            # modern resumptive structure
            if is_resumptive_in_final_clause and is_main_clause_go:
                mccloskey_parsed_s.set_comp(0, GO_MODERN_RESUMPTIVE_TAG)
            # resumptive structure
            elif is_resumptive_in_final_clause and is_main_clause_a and is_go_in_embedded_clauses:
                mccloskey_parsed_s.set_comp(0, A_RESUMPTIVE_TAG)
            # gap structure
            elif is_gap_structure and not is_resumptive_in_final_clause:
                # for every clause except the final one
                for i in range(n_clauses-1):
                    # change the selected comp to aL instead of a
                    mccloskey_parsed_s.set_comp(i, A_GAP_TAG)
            else:
                # for every clause except the final one
                for i in range(n_clauses-1):
                    # change the selected comp to aL instead of a
                    clause_comp = mccloskey_parsed_s.get_comp(i)
                    if clause_comp == "a":
                        mccloskey_parsed_s.set_comp(i, A_GAP_TAG)
        else:
            return ps
        return mccloskey_parsed_s

    def parse_from_json(self, path: str):
        parsed_sentences = self.clause_parser.read_from(path)
        mccloskey_sentences = []
        for sentence in parsed_sentences:
            mccloskey_ps = self.parse(sentence)
            mccloskey_sentences.append(mccloskey_ps)
        return mccloskey_sentences

    def parse_to_str(self, sentence: ParsedSentence):
        mccloskey_parsed_sentence = self.parse(sentence)
        n_clauses = mccloskey_parsed_sentence.get_num_clauses()
        result = ""

        if not mccloskey_parsed_sentence or n_clauses <= 1:
            return "[ ]"

        for i,clause in enumerate(mccloskey_parsed_sentence):
            if i == 0:
                result += clause["preceding_category"] + " "
            
            comp = clause["selected_comp"]
            if comp:
                result += comp + " [ "
        return result

def main():
    parser = McCloskeyParser()
    example = "An fhilíocht a chum sí."
    parsed = parser.parse_to_str(example)
    print(parsed)

    mccloskey_data_path = "data/mccloskey-complementiser-data.csv"
    mccloskey_data = pd.read_csv(mccloskey_data_path, header=0)
    irish_sentences = list(mccloskey_data['sentence_irish'])
    english_translations = list(mccloskey_data['sentence_english'])
    parsed_sentences = []

    for sentence in irish_sentences:
        parsed = parser.parse_to_str(sentence)
        parsed_sentences.append(parsed)

    for i, ps in enumerate(parsed_sentences):
        print(irish_sentences[i])
        print(english_translations[i])
        print(ps)

if __name__ == "__main__":
    main()


            


