from spacy.lang.ga.lemmatizer import demutate
from spacy.lang.ga import Irish

class IrishLemmatiser:
    def __init__(self):
        self.nlp_ga = Irish()
        pass

    def __call__(self, sent: str):
        lemmatised_sent = []

        # convert to lowercase
        sent = sent.lower()

        # tokenise the sentence
        doc = self.nlp_ga(sent)

        # iterate through each token
        for t in doc:
            # lemmatise & store the token
            lemmatised = demutate(t.text)
            lemmatised_sent.append(lemmatised)
        return lemmatised_sent
