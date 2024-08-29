from ..preprocessing.string_manipulation import from_beginning_of_sentence, up_to_end_of_sentence
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

    def load_dataset(self, complementiser: str, region: str, nrows: int):
        dataset_path = self.datasets[complementiser][region]
        df = pd.read_csv(dataset_path, header=0, nrows=nrows)

        complementisers = df["KWIC"]
        left_relevant = [from_beginning_of_sentence(x) for x in df['Left']]
        right_relevant = [up_to_end_of_sentence(x) for x in df['Right']]
        full_sentence = [main + " " + comp + " " + emb for main, emb, comp in zip(left_relevant, right_relevant, complementisers)]


        df_processed = pd.DataFrame({
            "sentence": full_sentence,  
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
