from tools.syntax.parser import SentenceParser
import pandas as pd
import json

def main():
    mccloskey_data_path = "data/mccloskey-complementiser-data.csv"
    mccloskey_data = pd.read_csv(mccloskey_data_path, header=0)
    irish_sentences = list(mccloskey_data['sentence_irish'])
    english_translations = list(mccloskey_data['sentence_english'])
    sentence_parser = SentenceParser()
    parsed_sentences = []

    for sentence in irish_sentences:
        parsed = sentence_parser(sentence)
        parsed_sentences.append(parsed)

    for i, ps in enumerate(parsed_sentences):
        ps["english_translation"] = english_translations[i]

    with open('data/results/clause_info.json', 'w', encoding='utf-8') as file:
        json.dump(parsed_sentences, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()