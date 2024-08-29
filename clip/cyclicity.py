from .tools.syntax.complementisers import ComplementiserAnalyser
from .tools.morphology.lemmatiser import IrishLemmatiser
import pandas as pd

comp_analyser = ComplementiserAnalyser()
lemmatiser = IrishLemmatiser()

def main():
    mccloskey_data_path = "data/mccloskey-complementiser-data.csv"
    mccloskey_data = pd.read_csv(mccloskey_data_path, header=0)
    irish_sentences = list(mccloskey_data['sentence_irish'])
    print(mccloskey_data.head())

    for s in irish_sentences:
        lemmas = lemmatiser(s)
        clauses = comp_analyser.get_comp_clauses(lemmas)
        clause_as_str = comp_analyser.get_comp_clauses_as_str(lemmas)

        # print the results
        print("Full Sentence: ", s)
        print("Lemmas: ", lemmas)
        print("Parsed: ", clause_as_str)
        
        print("\n\n")
        print("Next Clause")
        print("\n\n")


if __name__=="__main__":
    main()