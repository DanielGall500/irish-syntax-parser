from tools.classifier import IrishComplementiserClassifier
from tools.lemmatiser import IrishLemmatiser
from tools.pos_tagger import POSTagger
import pandas as pd

def main():
    df_connacht = pd.read_csv("data/dialect/go_connacht_dataset_100.csv", header=0)
    df_munster = pd.read_csv("data/dialect/go_munster_dataset_100.csv", header=0)
    df_ulster = pd.read_csv("data/dialect/go_ulster_dataset_100.csv", header=0)
    datasets = [df_connacht, df_munster, df_ulster]

    for ds in datasets:
        ds["full_sentence"] = ds["Left"].str.cat([ds["KWIC"], ds["Right"]], sep=" ")

        # Filter to remove GO adjectives
        tagger = POSTagger()
        is_adjective = ds.apply(tagger.is_adjective, axis=1)
        ds = ds[~is_adjective]

        is_noun = ds.apply(tagger.preceded_by_noun, axis=1)
        ds['preceded_by_noun'] = is_noun

        for x,y in zip(ds['Left'], ds['preceded_by_noun']):
            print(x[-10:])
            print(y)
            print("----")

        print(ds['preceded_by_noun'].describe())
        import sys
        sys.exit(0)

        comp_classifier = IrishComplementiserClassifier()

        # tokenisation & lemmatisation process
        irish_sentences = ds['full_sentence']
        lemmatiser = IrishLemmatiser()
        lemmatised_data = []
        for s in irish_sentences:
            lemmatised_sent = lemmatiser(s)
            lemmatised_data.append(lemmatised_sent)

        occurrences = comp_classifier.get().get_sum_of_occurrences(lemmatised_data)
        print(occurrences)

        """
        for lemma_sent in lemmatised_data:
            occurrences = 
            particle_matrix = comp_classifier(lemma_sent)
            print(particle_matrix)
            sums = np.sum(particle_matrix, axis=1)
            complementiser_sums = np.add(complementiser_sums, sums)
            print(complementiser_sums)

            print("----")
            print("Sentence: ", lemma_sent)
            print("Matrix\n", particle_matrix)
            print("----")
        """

if __name__ == "__main__":
    main()