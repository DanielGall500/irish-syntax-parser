from tools.lemmatiser import IrishLemmatiser
import pandas as pd

# this is too specific to the format of the CSV file
class POSTagger:
    def __init__(self):
        adjectives = pd.read_csv("data/POS/focloir_adjectives.csv")
        adj_list = list(adjectives['Item'])
        self.adj_lookup = {adj:True for adj in adj_list}

        nouns = pd.read_csv("data/POS/focloir_nouns.csv")
        noun_list = list(nouns['Item'])
        self.noun_lookup = {noun:True for noun in noun_list}

        self.lemmatiser = IrishLemmatiser()

    # these functions should be improved 
    def is_adjective(self, row):
        # does not take into account when the adjective
        # looks like a noun.
        right_of_comp = row['Right'].lower()
        if len(right_of_comp) > 0:
            lemmatised = self.lemmatiser(right_of_comp)
            first_lemma = lemmatised[0]
            return self.is_POS(first_lemma, self.adj_lookup)
        return False

    def preceded_by_noun(self, row):
        left_of_comp = row['Left'].lower()
        if len(left_of_comp) > 0:
            lemmatised = self.lemmatiser(left_of_comp)
            final_lemma = lemmatised[-1]
            return self.is_POS(final_lemma, self.noun_lookup)

    def is_POS(self, word, POS_lookup):
        return word in POS_lookup