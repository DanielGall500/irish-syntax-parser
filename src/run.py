from tools.syntax.complementisers import ComplementiserAnalyser
from preprocessing.row_manipulation import to_lemmas
from preprocessing.string_manipulation import from_beginning_of_sentence, up_to_end_of_sentence
import pandas as pd

ANALYSE_GO = True

if ANALYSE_GO:
    CONNACHT_DATASET = "data/dialect/go_connacht_dataset_80k.csv"
    MUNSTER_DATASET = "data/dialect/go_munster_dataset_80k.csv"
    ULSTER_DATASET = "data/dialect/go_ulster_dataset_80k.csv"
else:
    CONNACHT_DATASET = "data/dialect/a_connacht_dataset_100k.csv"
    MUNSTER_DATASET = "data/dialect/a_munster_dataset_100k.csv"
    ULSTER_DATASET = "data/dialect/a_ulster_dataset_100k.csv"

comp_analyser = ComplementiserAnalyser()

def main():
    # -- Step 1: Store the data from each region. --
    df_connacht = pd.read_csv(CONNACHT_DATASET, header=0, nrows=500)
    df_munster = pd.read_csv(MUNSTER_DATASET, header=0, nrows=500)
    df_ulster = pd.read_csv(ULSTER_DATASET, header=0, nrows=500)
    datasets = [df_connacht, df_munster, df_ulster]
    datasets = {
        "Connacht": df_connacht,
        "Munster": df_munster,
        "Ulster": df_ulster
    }

    # -- Step 2: Perform pre-processing on each dataset. --
    for title in datasets.keys():
        ds = datasets[title]
        main_clauses = [from_beginning_of_sentence(x) for x in ds['Left']]
        embedded_clauses = [up_to_end_of_sentence(x) for x in ds['Right']]
        comps = ds['KWIC']

        full_sentence = [main + " " + comp + " " + emb for main, emb, comp in zip(main_clauses, embedded_clauses, comps)]

        datasets[title]["main_clause"] = main_clauses
        datasets[title]["embedded_clause"] = embedded_clauses
        datasets[title]["complementiser"] = comps
        datasets[title]["full_sentence"] = full_sentence

        linguistic_analysis = run_syntactic_analysis(ds)
        datasets[title]["followed_by_adj"] = linguistic_analysis["followed_by_adjective"] 
        datasets[title]["preceded_by_noun"] = linguistic_analysis["preceded_by_noun"] 
        datasets[title]["followed_by_number"] = linguistic_analysis["followed_by_number"] 
        datasets[title]["resumptive_found"] = linguistic_analysis["resumptive_found"] 
        datasets[title]["resumptive"] = linguistic_analysis["resumptive"] 

        print(ds.head())

    # -- Step 3: Run the syntactic analysis. --
    for title in datasets.keys():
        ds = datasets[title]
        followed_by_adj_feature = ds["followed_by_adj"]
        preceded_by_noun_feature = ds["preceded_by_noun"]
        followed_by_number_feature = ds["followed_by_number"]
        resumptive_found_feature = ds["resumptive_found"]

        if ANALYSE_GO:
            # REMOVE SENTENCES WITH ADJECTIVES FOLLOWING COMPLEMENTISER
            ds = ds[followed_by_adj_feature == False]

            # REMOVE SENTENCES WITH NUMBERS FOLLOWING COMPLEMENTISER
            ds = ds[followed_by_number_feature == False]

            # REMOVE SENTENCES WITH NOUN PRECEDING COMPLEMENTISER
            # This constraint can be removed.
            # Given that a noun precedes it, does it tend to contain a potential resumptive pronoun?
            # TODO: This should work through each clause in cycles.
            # ds = ds[preceded_by_noun_feature == True]

            # -- VIEW RESULTS -- 
            num_preceded = sum(preceded_by_noun_feature)
            percent_preceded = round(num_preceded / len(preceded_by_noun_feature) * 100,2)
            percent_resumptive = (sum(resumptive_found_feature) / len(resumptive_found_feature)) * 100
            print(f"DATASET: {title}")
            print("Preceded by noun?")
            print(preceded_by_noun_feature.value_counts())
            print(f"Percentage Preceded: {percent_preceded}")
            print(f"Percentage Containing Resumptive of the Noun-Preceding Comps: {percent_resumptive}")
        else:
            # -- TODO --
            # remove any complementisers followed by a number

            # FILTER: KEEP SENTENCES WITH NOUN PRECEDING COMPLEMENTISER
            ds = ds[preceded_by_noun_feature]

            # apply a filter depending on whether a resumptive
            # pronoun is present or not present
            # this distinguishes aN (resumptive) from aL (no resumptive)
            ds_resumptive = ds[resumptive_found_feature]
            ds_nonresumptive = ds[~resumptive_found_feature]
            view_data(title, ds_resumptive, ds_nonresumptive)


def run_syntactic_analysis(ds):
    is_followed_by_adjective = ds.apply(lemma_decorator, 
                                   axis=1, 
                                   args={ comp_analyser.is_followed_by_adjective  })

    is_preceded_by_noun = ds.apply(lemma_decorator, 
                                   axis=1, 
                                   args={ comp_analyser.is_preceded_by_noun  })

    is_followed_by_number = ds.apply(lemma_decorator, 
                                   axis=1, 
                                   args={ comp_analyser.is_followed_by_number  })

    resumptive_found = ds.apply(lemma_decorator, 
                                   axis=1, 
                                   args={ comp_analyser.contains_resumptive  })

    is_resumptive_found = resumptive_found.apply(lambda x: x['found'])
    resumptive_token = resumptive_found.apply(lambda x: x['lemma'])

    return {
        "followed_by_adjective": is_followed_by_adjective,
        "preceded_by_noun": is_preceded_by_noun,
        "followed_by_number": is_followed_by_number,
        "resumptive_found": is_resumptive_found,
        "resumptive": resumptive_token
    }

def lemma_decorator(row, func):
    lemmas = to_lemmas(row)
    comp_index = len(lemmas['main'])
    return func(lemmas["all"], comp_index)

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

if __name__ == "__main__":
    main()