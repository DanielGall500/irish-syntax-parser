from tools.classifier import IrishComplementiserClassifier
from tools.lemmatiser import IrishLemmatiser
from tools.pos_tagger import IrishPOSTagger
import pandas as pd

tagger = IrishPOSTagger()
lemmatiser = IrishLemmatiser()
eos_chars = ['.',',','?','!','-','\'', '>', '<']

def up_to_end_of_sentence(T: str) -> str:
    final_string = ""
    for c in T:
        if c not in eos_chars:
            final_string += c
        else:
            break
    return final_string

def from_beginning_of_sentence(T: str) -> str:
    final_string = ""
    i = len(T)-1
    while i >= 0:
        if T[i] in eos_chars:
            break
        final_string += T[i]
        i -= 1
    return final_string[::-1]

def is_comp_preceded_by_noun(row) -> bool:
    left_of_comp = row['Left'].lower()
    if len(left_of_comp) > 0:
        lemmatised = lemmatiser(left_of_comp)
        final_lemma = lemmatised[-1]
        return tagger.is_noun(final_lemma)
    return False

def contains_resumptive(row) -> bool:
    right_of_comp = row['Right'].lower()
    if len(right_of_comp) > 0:
        relevant_expression = up_to_end_of_sentence(right_of_comp)
        lemmatised = lemmatiser(relevant_expression)
        for lemma in lemmatised:
            if tagger.is_resumptive_pronoun(lemma):
                return True
        return False

def main():
    df_connacht = pd.read_csv("data/dialect/a_connacht_dataset_100.csv", header=0)
    df_munster = pd.read_csv("data/dialect/a_munster_dataset_100.csv", header=0)
    df_ulster = pd.read_csv("data/dialect/a_ulster_dataset_100.csv", header=0)
    datasets = [df_connacht, df_munster, df_ulster]
    datasets = {
        "Connacht": df_connacht,
        "Munster": df_munster,
        "Ulster": df_ulster
    }

    for title in datasets.keys():
        ds = datasets[title]
        ds["full_sentence"] = ds["Left"].str.cat([ds["KWIC"], ds["Right"]], sep=" ")

        # Filter to include only a complementisers which
        # are clearly preceded by a noun
        preceded_by_noun = ds.apply(is_comp_preceded_by_noun, axis=1)
        # ds['preceded_by_noun'] = is_noun
        ds = ds[preceded_by_noun]

        # Now we will filter to only find a complementisers
        # which include a resumptive pronoun anywhere in the
        # remaining sentence.
        resumptive_found = ds.apply(contains_resumptive, axis=1)
        ds = ds[resumptive_found]
        resumptives_found_as_percent = (resumptive_found.sum() / len(resumptive_found)) * 100
        print(resumptive_found.sum())
        print("----")
        print("Dataset: ", title)
        print("Number of Resumptives: ", round(resumptives_found_as_percent,2))
        print("Number of Non Resumptives: ", round(100.0 - resumptives_found_as_percent,2))
        print("----")

        """
        # We want to only include up to the full stop
        # as we just want the current relevant sentence
        # for the complementiser.
        for s_left, s_right in zip(ds['Left'], ds['Right']):
            print("\n")
            print(from_beginning_of_sentence(s_left) + " **a** " + up_to_end_of_sentence(s_right))
            print("\n")
        """

if __name__ == "__main__":
    main()