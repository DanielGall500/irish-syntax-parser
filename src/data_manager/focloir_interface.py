from preprocessing.string_manipulation import from_beginning_of_sentence, up_to_end_of_sentence
import pandas as pd

# all dataset paths
GO_CONNACHT_80k = "data/dialect/go_connacht_dataset_80k.csv"
GO_MUNSTER_80k = "data/dialect/go_munster_dataset_80k.csv"
GO_ULSTER_80k = "data/dialect/go_ulster_dataset_80k.csv"
A_CONNACHT_100k = "data/dialect/a_connacht_dataset_100k.csv"
A_MUNSTER_100k = "data/dialect/a_munster_dataset_100k.csv"
A_ULSTER_100k = "data/dialect/a_ulster_dataset_100k.csv"

class FocloirDataInterface:
    datasets = {
        "go": {
            "Connacht": GO_CONNACHT_80k,
            "Munster": GO_MUNSTER_80k,
            "Ulster": GO_ULSTER_80k
        },
        "a": {
            "Connacht": A_CONNACHT_100k,
            "Munster": A_MUNSTER_100k,
            "Ulster": A_ULSTER_100k
        },
        "all": {
            "Connacht": "",
            "Munster": "",
            "Ulster": "",
            "General": ""
        }
    }

    def load_dataset(self, complementiser: str, region: str):
        dataset_path = self.datasets[complementiser][region]
        df = pd.read_csv(dataset_path, header=0)

        complementiser = df["KWIC"].lower()
        left_relevant = [from_beginning_of_sentence(x) for x in df['Left']]
        right_relevant = [up_to_end_of_sentence(x) for x in df['Right']]
        full_sentence = df["left_relevant"].str.cat([df["KWIC"], df["right_relevant"]], sep=" ")

        # lemmatise everything
        left_lemmatised = [self.syntax_manager.lemmatiser(l_s) for l_s in left_relevant] 
        right_lemmatised = [self.syntax_manager.lemmatiser(r_s) for r_s in right_relevant]
        full_lemmatised = [self.syntax_manager.lemmatiser(full_s) for full_s in full_sentence]
        complementiser_lemma_index = [len(l_s) for l_s in left_relevant]

        # add relevant linguistic features
        noun_precedes_comp = []
        adj_follows_comp = []
        for full_s, comp_index in zip(full_sentence, complementiser_lemma_index):
            does_noun_precede_comp = self.syntax_manager.is_comp_preceded_by_noun(full_s, comp_index)
            does_adj_follow_comp = self.syntax_manager.is_followed_by_adjective(full_s, comp_index)

            noun_precedes_comp.append(does_noun_precede_comp[0])
            adj_follows_comp.append(does_adj_follow_comp[0])

        df_processed = pd.DataFrame({
            "comp": complementiser,
            "left": left_relevant, 
            "right": right_relevant, 
            "full": full_sentence,
            "left_lemmatised": left_lemmatised,
            "right_lemmatised": right_lemmatised,
            "full_lemmatised": full_lemmatised,
            "complementiser_index": complementiser_lemma_index,
            "preceded_by_noun": noun_precedes_comp,
            "followed_by_adj": adj_follows_comp,
        })
        return df_processed

"""
-- Focloir Lookup Function --
Focloir is a well-known dictionary for the Irish language.
This function returns a lookup dictionary containing all words in the
focloir dictionary and can be used to check whether words are recognised
as Irish from a string.
It should only be called once in each run.
"""
def get_lexical_items_from_focloir(path: str) -> dict:
    focloir_dataset = pd.read_csv(path)
    focloir_words = list(focloir_dataset['Item'])
    return focloir_words
