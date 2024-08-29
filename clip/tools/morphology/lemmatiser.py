from spacy.lang.ga.lemmatizer import demutate
from spacy.lang.ga import Irish

"""
-- Irish Lemmatiser --
Input: String which should represent an Irish sentence.
Output: A list of strings representing the lemmas of the sentence.

What is lemmatisation?
A lemma is the dictionary or base form of a group of lexical items. 
For instance, the word "swim" is the base word for the form "swimming", "swam", etc.
It is often more complex than simply stemming, for instance the lemma of "better" would be "good".
This is known as suppletion and must also be taken into account when building a lemmatiser.

What does this class do?
1. Take a string as input.
2. Convert the string to lowercase.
3. Tokenise the sentence primarily into individual words.
4. Iterate through each token and lemmatise it (the demutate function).
5. A list of these lemmas is returned as output.
"""
class IrishLemmatiser:
    def __init__(self):
        self.nlp_ga = Irish()
        pass

    def __call__(self, sent: str):
        lemmatised_sent = []

        if sent:
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
