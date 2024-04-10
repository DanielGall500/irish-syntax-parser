from tools.classifier import IrishComplementiserClassifier
from tools.lemmatiser import IrishLemmatiser
from tools.pos_tagger import IrishPOSTagger
import pandas as pd

tagger = IrishPOSTagger()
lemmatiser = IrishLemmatiser()

print("Starting 1...")
def is_followed_by_adjective(row):
    # does not take into account when the adjective
    # looks like a noun.
    right_of_comp = row['Right'].lower()
    if len(right_of_comp) > 0:
        lemmatised = lemmatiser(right_of_comp)
        first_lemma = lemmatised[0]
        return tagger.is_adjective(first_lemma)
    return False
print("Starting 2...")

def main():
    df_connacht = pd.read_csv("data/dialect/go_connacht_dataset_100.csv", header=0)
    df_munster = pd.read_csv("data/dialect/go_munster_dataset_100.csv", header=0)
    df_ulster = pd.read_csv("data/dialect/go_ulster_dataset_100.csv", header=0)
    datasets = [df_connacht, df_munster, df_ulster]

    for ds in datasets:
        print("Starting 3...")
        ds["full_sentence"] = ds["Left"].str.cat([ds["KWIC"], ds["Right"]], sep=" ")

        # Filter to remove GO adjectives
        is_adjective = ds.apply(is_followed_by_adjective, axis=1)
        ds = ds[~is_adjective]

if __name__ == "__main__":
    main()