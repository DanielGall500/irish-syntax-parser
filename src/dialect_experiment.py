from tools.syntax.parser import SentenceParser, ParsedSentence
from preprocessing.string_manipulation import json_path_builder
from collections import deque

def analyse_noun_before_go(sentences: list[ParsedSentence]):
    nouns_before_comp_counter = 0
    total_clauses_counter = 0
    for sentence in sentences:
        for clause in sentence:
            if clause["noun_final"]:
                nouns_before_comp_counter += 1
            total_clauses_counter += 1

    print(f"Number of complementisers preceded by noun: {nouns_before_comp_counter}")
    print(f"Number of clauses: {total_clauses_counter}")
    print(f"Percentage: {(nouns_before_comp_counter / total_clauses_counter) * 100}")

def analyse_a(sentences: list[ParsedSentence]):
    # apply a filter depending on whether a resumptive
    # pronoun is present or not present
    # this distinguishes aN (resumptive) from aL (no resumptive)

    # number of sentences where a resumptive pronoun
    # appears in the last clause
    res_pronoun_counter = 0
    n_sentences = len(sentences)
    for sentence in sentences:
        n_clauses = sentence.get_num_clauses()
        if n_clauses > 1:
            final_clause = deque(sentence, maxlen=1)[0]
            if final_clause["is_resumptive_found"]:
                res_pronoun_counter += 1

    print(f"Number of resumptive final comps found: {res_pronoun_counter}")
    print(f"Number of sentences: {n_sentences}")
    print(f"PERCENTAGE: {(res_pronoun_counter / n_sentences) * 100}%")

def main():
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
    for dataset in datasets:
        comp = dataset[0]
        region = dataset[1]
        path = json_path_builder(comp, region)
        parsed_sentences = sentence_parser.read_from(path)
        parsed_sentences = [ParsedSentence(sentence) for sentence in parsed_sentences]

        print("Dataset: {}, {}".format(comp, region))
        if comp == "go":
            analyse_noun_before_go(parsed_sentences)
        elif comp == "a":
            analyse_a(parsed_sentences)
        else:
            print("Invalid complementiser.")

if __name__ == "__main__":
    main()