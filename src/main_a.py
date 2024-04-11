from tools.lemmatiser import IrishLemmatiser
from tools.pos_tagger import IrishPOSTagger
import pandas as pd

tagger = IrishPOSTagger()
lemmatiser = IrishLemmatiser()
eos_chars = ['.',',','?','!','-','\'', '>', '<']

def filter_resumptive(ds):
    # -- TODO --
    # remove any complementisers followed by
    # a number

    # -- FILTER: Preceded by noun --
    # Filter to include only a complementisers which
    # are clearly preceded by a noun
    is_preceded_by_noun = ds.apply(is_comp_preceded_by_noun, axis=1)
    ds = ds[is_preceded_by_noun]

    # -- FILTER: Resumptive / Non-Resumptive
    # Now we will filter to only find a complementisers
    # which include a resumptive pronoun anywhere in the
    # remaining sentence.
    resumptive_found = ds.apply(contains_resumptive, result_type="expand", axis=1)
    is_resumptive_found = resumptive_found[0]
    resumptive_token = resumptive_found[1]

    ds['is_resumptive_found'] = is_resumptive_found
    ds['resumptive'] = resumptive_token

    ds_resumptive = ds[is_resumptive_found]
    ds_nonresumptive = ds[~is_resumptive_found]

    return ds_resumptive, ds_nonresumptive

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
    left_of_comp = row['left_relevant'].lower()
    if len(left_of_comp) > 0:
        lemmatised = lemmatiser(left_of_comp)
        final_lemma = lemmatised[-1]
        return tagger.is_noun(final_lemma)
    return False

def contains_resumptive(row) -> list:
    right_of_comp = row['right_relevant'].lower()
    if len(right_of_comp) > 0:
        lemmatised = lemmatiser(right_of_comp)
        for lemma in lemmatised:
            if tagger.is_resumptive_pronoun(lemma):
                return [True,lemma]
    return [False,""]

def view_data(title, resumptives, non_resumptives):
    num_resumptives = len(resumptives)
    num_non_resumptives = len(non_resumptives)
    resumptives_found_as_percent = num_resumptives / (num_resumptives + num_non_resumptives) * 100
    print("----")
    print("Dataset: ", title)
    print("Number of Resumptives: ", round(resumptives_found_as_percent,2))
    print("Number of Non Resumptives: ", round(100.0 - resumptives_found_as_percent,2))
    print(f"Resumptive Statistics: \n {resumptives['resumptive'].value_counts()}")

    # We want to only include up to the full stop
    # as we just want the current relevant sentence
    # for the complementiser.
    datasets = {
        "RESUMPTIVE": resumptives,
        "NON_RESUMPTIVE": non_resumptives
    }
    for title in datasets.keys():
        counter = 0
        ds = datasets[title]
        print(f"\n{title} Examples")
        for sentence in ds['full_sentence']:
            counter += 1
            print("\n")
            print(sentence)
            print("\n")

            if counter == 5:
                break
    print("----\n")

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
        ds["left_relevant"] = [from_beginning_of_sentence(x) for x in ds['Left']]
        ds["right_relevant"] = [up_to_end_of_sentence(x) for x in ds['Right']]
        ds["full_sentence"] = ds["left_relevant"].str.cat([ds["KWIC"], ds["right_relevant"]], sep=" ")

        # -- RESUMPTIVE / NON-RESUMPTIVE SEARCH --
        # find the resumptive and non-resumptive complementiser
        # sentences in the dataset
        ds_resumptive, ds_nonresumptive = filter_resumptive(ds)
        view_data(title, ds_resumptive, ds_nonresumptive)

if __name__ == "__main__":
    main()