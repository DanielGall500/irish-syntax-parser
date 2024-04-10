from tools.classifier import IrishComplementiserClassifier
from tools.lemmatiser import IrishLemmatiser
from tools.pos_tagger import IrishPOSTagger
import pandas as pd

tagger = IrishPOSTagger()
lemmatiser = IrishLemmatiser()

def up_to_end_of_sentence(T):
    final_string = ""
    eos_chars = ['.',',','?','!','-','\'']
    for c in T:
        if c not in eos_chars:
            final_string += c
        else:
            break
    return final_string

def is_comp_preceded_by_noun(row):
    left_of_comp = row['Left'].lower()
    if len(left_of_comp) > 0:
        lemmatised = lemmatiser(left_of_comp)
        final_lemma = lemmatised[-1]
        return tagger.is_noun(final_lemma)
    return False

def main():
    df_connacht = pd.read_csv("data/dialect/a_connacht_dataset_100.csv", header=0)
    df_munster = pd.read_csv("data/dialect/a_munster_dataset_100.csv", header=0)
    df_ulster = pd.read_csv("data/dialect/a_ulster_dataset_100.csv", header=0)
    datasets = [df_connacht, df_munster, df_ulster]

    for ds in datasets:
        ds["full_sentence"] = ds["Left"].str.cat([ds["KWIC"], ds["Right"]], sep=" ")

        # Filter to include only a complementisers which
        # are clearly preceded by a noun
        preceded_by_noun = ds.apply(is_comp_preceded_by_noun, axis=1)
        # ds['preceded_by_noun'] = is_noun
        ds = ds[preceded_by_noun]

        # We want to only include up to the full stop
        # as we just want the current relevant sentence
        # for the complementiser.
        for s_left, s_right in zip(ds['Left'], ds['Right']):
            print("----")
            print(s_left)
            print(up_to_end_of_sentence(s_right))
            print("----")

if __name__ == "__main__":
    main()