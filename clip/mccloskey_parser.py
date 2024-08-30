from .tools.syntax.parser import IrishClauseParser, ParsedSentence
import pandas as pd

class McCloskeyParser:
    def __init__(self):
        self.clause_parser = IrishClauseParser()

    def __call__(self, sentence: str):
        parsed_sentence = self.clause_parser(sentence)
        mccloskey_parsed_s = parsed_sentence
        n_clauses = parsed_sentence.get_num_clauses()

        if n_clauses > 1:
            selected_comps = []
            XP_preceding_comps = []
            resumptives = []
            for i,clause in enumerate(parsed_sentence):
                category = "DP" if clause["noun_final"] else "XP"
                mccloskey_parsed_s[i]["preceding_category"] = category
                resumptives.append(clause["is_resumptive_found"])
                del mccloskey_parsed_s[i]["noun_final"]
                del mccloskey_parsed_s[i]["adj_initial"]
                del mccloskey_parsed_s[i]["number_initial"]

                comp = clause["selected_comp"]

                # REPLACE WITH LANGUAGE DATA
                if comp:
                    if comp in ["go", "gur"]:
                        comp = "go"
                        mccloskey_parsed_s[i]["selected_comp"] = "go"
                    XP_preceding_comps.append(category)
                    selected_comps.append(comp)

            # modern resumptive structure
            if resumptives[-1] and selected_comps[0] == "go":
                mccloskey_parsed_s[0]["selected_comp"] = "goN"
            # resumptive structure
            elif resumptives[-1] and selected_comps[0] == "a":
                mccloskey_parsed_s[0]["selected_comp"] = "aN"
            # gap structure
            elif all(c == "a" for c in selected_comps) and resumptives[-1] == False:
                # for every clause except the final one
                for i in range(n_clauses-1):
                    # change the selected comp to aL instead of a
                    mccloskey_parsed_s[i]["selected_comp"] = "aL"
            else:
                # for every clause except the final one
                for i in range(n_clauses-1):
                    # change the selected comp to aL instead of a
                    if mccloskey_parsed_s[i]["selected_comp"] == "a":
                        mccloskey_parsed_s[i]["selected_comp"] = "aL"

        else:
            return parsed_sentence
        return mccloskey_parsed_s

    def parse_to_str(self, sentence: str):
        mccloskey_parsed_sentence = self.__call__(sentence)
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


            


