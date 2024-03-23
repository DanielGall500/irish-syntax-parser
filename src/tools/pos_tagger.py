from tools.lemmatiser import IrishLemmatiser
import pandas as pd

class POSTagger:
    def __init__(self):
        adjectives = pd.read_csv("data/POS/focloir_adjectives.csv")
        adj_list = list(adjectives['Item'])
        self.adj_lookup = {adj:True for adj in adj_list}

        self.lemmatiser = IrishLemmatiser()

    def is_adjective(self, row):
        # does not take into account when the adjective
        # looks like a noun.
        right_of_comp = row['Right']
        if len(right_of_comp) > 0:
            lemmatised = self.lemmatiser(right_of_comp)
            return lemmatised[0] in self.adj_lookup

