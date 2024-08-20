from tools.syntax import SyntaxManager
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

syntax_manager = SyntaxManager()

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

        print(ds.head())

    # -- Step 3: Run the syntactic analysis. --
    for title in datasets.keys():
        ds = datasets[title]
        linguistic_analysis = run_syntactic_analysis(ds)

        if ANALYSE_GO:
            # REMOVE SENTENCES WITH ADJECTIVES FOLLOWING COMPLEMENTISER
            followed_by_adj = linguistic_analysis["followed_by_adjective"] 
            ds = ds[~followed_by_adj]

            # REMOVE SENTENCES WITH NOUN PRECEDING COMPLEMENTISER
            # This constraint can be removed.
            # Given that a noun precedes it, does it tend to contain a potential resumptive pronoun?
            # TODO: This should work through each clause in cycles.
            preceded_by_noun = linguistic_analysis["preceded_by_noun"] 
            ds = ds[preceded_by_noun]

            is_resumptive_found = linguistic_analysis["resumptive_found"]

            # -- VIEW RESULTS -- 
            print(f"DATASET: {title}")
            print("Preceded by noun?")
            num_preceded = sum(preceded_by_noun)
            percent_preceded = round(num_preceded / len(preceded_by_noun) * 100,2)
            print(preceded_by_noun.value_counts())
            print(f"Percentage Preceded: {percent_preceded}")
            percent_resumptive = (sum(is_resumptive_found) / len(is_resumptive_found)) * 100
            print(f"Percentage Containing Resumptive of the Noun-Preceding Comps: {percent_resumptive}")
        else:
            followed_by_adj = linguistic_analysis["followed_by_adjective"] 

            # -- TODO --
            # remove any complementisers followed by
            # a number

            # FILTER: KEEP SENTENCES WITH NOUN PRECEDING COMPLEMENTISER
            preceded_by_noun = linguistic_analysis["preceded_by_noun"] 
            print("PRECEDED BY NOUN?")
            ds = ds[preceded_by_noun]

            # -- FILTER: Resumptive / Non-Resumptive
            # Now we will filter to only find a complementisers
            # which include a resumptive pronoun anywhere in the
            # remaining sentence.

            resumptive_found = linguistic_analysis["resumptive_found"]
            resumptives = linguistic_analysis["resumptive"]

            print(resumptive_found)
            ds['is_resumptive_found'] = resumptive_found
            ds['resumptive'] = resumptives

            # apply a filter depending on whether a resumptive
            # pronoun is present or not present
            # this distinguishes aN (resumptive) from aL (no resumptive)
            ds_resumptive = ds[resumptive_found]
            ds_nonresumptive = ds[~resumptive_found]
            view_data(title, ds_resumptive, ds_nonresumptive)


def run_syntactic_analysis(ds):
    is_followed_by_adjective = ds.apply(lemma_decorator, 
                                   axis=1, 
                                   args={ syntax_manager.is_followed_by_adjective  })

    is_preceded_by_noun = ds.apply(lemma_decorator, 
                                   axis=1, 
                                   args={ syntax_manager.is_comp_preceded_by_noun  })

    resumptive_found = ds.apply(lemma_decorator, 
                                   axis=1, 
                                   args={ syntax_manager.contains_resumptive  })

    is_resumptive_found = resumptive_found.apply(lambda x: x['found'])
    resumptive_token = resumptive_found.apply(lambda x: x['lemma'])

    return {
        "followed_by_adjective": is_followed_by_adjective,
        "preceded_by_noun": is_preceded_by_noun,
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