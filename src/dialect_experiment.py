from tools.syntax.complementisers import ComplementiserAnalyser
from preprocessing.row_manipulation import to_lemmas
from preprocessing.string_manipulation import from_beginning_of_sentence, up_to_end_of_sentence
from data_manager.focloir_interface import FocloirDataInterface
from parse import SentenceParser

def main():
    focloir_interface = FocloirDataInterface()
    sentence_parser = SentenceParser()

    # -- Step 1: Store the data from each region. --
    datasets = [
        ("go", "Connacht"),
        ("go", "Munster"),
        ("go", "Ulster"),
        ("a", "Connacht"),
        ("a", "Munster"),
        ("a", "Ulster")
    ]
    print("Loading in datasets")
    nrows = 10
    datasets_loaded = {
        "go": {},
        "a": {}
    }
    for dataset in datasets:
        comp = dataset[0]
        region = dataset[1]
        print("DATASET ", comp, region)
        df = focloir_interface.load_dataset(comp, region, nrows)
        sentences = df["sentence"]

        parsed_sentences = []
        for s in sentences:
            parsed_s = sentence_parser(s)
            parsed_sentences.append(parsed_s) 
        
        datasets_loaded[comp][region] = parsed_sentences

    # -- Step 2: Perform pre-processing on each dataset. --
    print(datasets_loaded.keys())
    for comp in datasets_loaded.keys():
        print(f"Checking Comp: {comp}")
        for region in datasets_loaded[comp].keys():
            print(f"Checking Region: {region}")
            ds = datasets_loaded[comp][region]

            # Analysis of sentences
            if comp == "go":
                nouns_before_comp_counter = 0
                total_clauses_counter = 0
                for sentence in ds:
                    clause_structure = sentence["clause_structure"]

                    num_clauses = sentence["num_clauses"]
                    total_clauses_counter += num_clauses

                    curr_clause = clause_structure
                    for i in range(num_clauses):
                        if curr_clause["noun_final"]:
                            nouns_before_comp_counter += 1
                        curr_clause = curr_clause["embedded_clause"]

                print(f"DATASET: {comp}, {region}")
                print(f"Number of complementisers preceded by noun: {nouns_before_comp_counter}")
                print(f"Number of clauses: {total_clauses_counter}")
                print(f"Percentage: {(nouns_before_comp_counter / total_clauses_counter) * 100}")
            else:
                # apply a filter depending on whether a resumptive
                # pronoun is present or not present
                # this distinguishes aN (resumptive) from aL (no resumptive)

                # number of sentences where a resumptive pronoun
                # appears in the last clause
                res_pronoun_counter = 0
                n_sentences = len(ds)
                for sentence in ds:
                    clause_structure = sentence["clause_structure"]
                    num_clauses = sentence["num_clauses"]

                    curr_clause = clause_structure
                    for i in range(num_clauses-1):
                        print(curr_clause["embedded_clause"])
                        curr_clause = curr_clause["embedded_clause"]
                    if curr_clause["is_resumptive_found"]:
                        res_pronoun_counter += 1
                    
                    print(f"DATASET: {comp}, {region}")
                    print(f"Number of resumptive final comps found: {res_pronoun_counter}")
                    print(f"Number of sentences: {n_sentences}")
                    print(f"Ratio: {(res_pronoun_counter / n_sentences) * 100}")


if __name__ == "__main__":
    main()