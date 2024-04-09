from tools.classifier import IrishComplementiserClassifier
from tools.lemmatiser import IrishLemmatiser
from tools.pos_tagger import POSTagger
import pandas as pd

def up_to_end_of_sentence(T):
    final_string = ""
    eos_chars = ['.',',','?','!','-','\'']
    for c in T:
        if c not in eos_chars:
            final_string += c
        else:
            break
    return final_string

def main():
    df_connacht = pd.read_csv("data/dialect/a_connacht_dataset_100.csv", header=0)
    df_munster = pd.read_csv("data/dialect/a_munster_dataset_100.csv", header=0)
    df_ulster = pd.read_csv("data/dialect/a_ulster_dataset_100.csv", header=0)
    datasets = [df_connacht, df_munster, df_ulster]

    for ds in datasets:
        ds["full_sentence"] = ds["Left"].str.cat([ds["KWIC"], ds["Right"]], sep=" ")

        tagger = POSTagger()

        # Filter to include only a complementisers which
        # are clearly preceded by a noun
        preceded_by_noun = ds.apply(tagger.preceded_by_noun, axis=1)
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

        """
        for x,y in zip(ds['Left'], ds['preceded_by_noun']):
            print(x[-10:])
            print(y)
            print("----")

        print(ds['preceded_by_noun'].describe())
        """

if __name__ == "__main__":
    main()