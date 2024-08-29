from .tools.syntax.matcher import ComplementiserMatcher

matcher = ComplementiserMatcher()

class Pattern:
    def __init__(self, lemmas: list[str]):
        self.lemmas = lemmas
        self.comps = matcher(lemmas)
        self.pattern = None


"""
-- Ideal Pattern --

Naive assumptions:
Run this only on the dataset in which anything which is not containing an
actual complementiser has been removed.
Each clause represents a deeper embedding.

Creidim gur inis se breag.

go: 0, 1, 0, 0, 0
aN: 0, 0, 0, 0, 0
aL: 0, 0, 0, 0, 0
RS: 0, 0, 0, 0, 0

Can then be flattened into:

0, go, 0, 0, 0

Pattern Object:
Lemmas: [creidim, gur, inis, se, breag]
Comps: [0, go, 0, 0, 0]
Pattern: [creidim, [go, inis, se, breag]]

How do we test for aN vs aL?
First Check: Is it "ar", then definitely aN.

No?
Is everything after a or is there go?
If yes, then it might be aN.

Still not sure?
Is there something after that looks like a resumptive pronoun in the final clause?
If yes, then it might be aN.

Once we arrive at this pattern formation, the hard work should be done.



"""
