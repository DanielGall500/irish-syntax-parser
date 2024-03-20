from classifier import IrishComplementiserClassifier
from spacy.lang.ga.lemmatizer import demutate
from spacy.lang.ga import Irish
import pandas as pd

def main():
    df = pd.read_csv("data/mccloskey-complementiser-data.csv", header=0)
    print(df)

    nlp_ga = Irish()
    comp_classifier = IrishComplementiserClassifier(nlp=nlp_ga)

    irish_sentences = df['sentence_irish']
    lemmatised_data = []
    for s in irish_sentences:
        lemmatised_sent = []
        doc = nlp_ga(s)
        for s_tokenised in doc:
            lemmatised = demutate(s_tokenised.text)
            lemmatised_sent.append(lemmatised)
        lemmatised_data.append(lemmatised_sent)

    for lemma_sent in lemmatised_data:
        particle_matrix = comp_classifier(lemma_sent)
        print("----")
        print("Sentence: ", lemma_sent)
        print("Matrix\n", particle_matrix)
        print("----")

if __name__ == "__main__":
    main()