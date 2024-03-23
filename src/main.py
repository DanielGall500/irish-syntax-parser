from tools.classifier import IrishComplementiserClassifier
from tools.lemmatiser import IrishLemmatiser
from tools.pos_tagger import POSTagger
import pandas as pd

def main():
    df = pd.read_csv("data/mccloskey-complementiser-data.csv", header=0)
    df_connacht = pd.read_csv("data/dialect/go_connacht_dataset.csv", header=0)
    print(df_connacht.head())

    # filter for GO adjectives
    tagger = POSTagger()
    go_connact_is_adjective = df_connacht.apply(tagger.is_adjective, axis=1)
    df_connacht = df_connacht[~go_connact_is_adjective]

    comp_classifier = IrishComplementiserClassifier()

    # tokenisation & lemmatisation process
    irish_sentences = df['sentence_irish']
    lemmatiser = IrishLemmatiser()
    lemmatised_data = []
    for s in irish_sentences:
        lemmatised_sent = lemmatiser(s)
        lemmatised_data.append(lemmatised_sent)

    for lemma_sent in lemmatised_data:
        particle_matrix = comp_classifier(lemma_sent)
        print("----")
        print("Sentence: ", lemma_sent)
        print("Matrix\n", particle_matrix)
        print("----")

if __name__ == "__main__":
    main()