# Automatic POS-tagging of Irish Complementisers
Irish is a highly inflectional Celtic language with Verb-Subject-Object (VSO) word order. In this research we will examine the Irish complementisers and their unique properties when it comes to long-distance dependencies, such as in the sentence *"He’s the guy that they said they thought they wanted to hire __"*, where long-distance movement has taken place from the original position of "the guy" after "hire". Irish has two strategies in order to model this type of long-distance dependency:
1. Movement takes place as in the example above and you are left with a trace (unfilled space).
2. Use a resumptive pronoun which provides an indication back to what is being referred to. Resumptive pronouns are not typical in English, but can still be expressed. For instance, in the sentence "This is the girl that whenever it rains she cries." Here, "she" acts as the resumptive pronoun, restating the person on whom an action is being completed.

#### Forms of Irish Complementisers
We begin with finite complement clauses, which is the simplest case where there are no long-distance dependencies. The particle used here is termed the **go** particle, which can surface in various ways due to it taking tense marking. For instance, in the following example the *go* particle takes a past-tense marking *r*:
```
Creidim gu-r inis sé bréag. 
I-believe go–[PAST] tell he lie 
‘I believe that he told a lie.’
```

Any finite clause which contains a trace due to non-local movement is introduced using a different particle, one which is termed **aL** (expressed as 'a').
We can see an example of this below with a trace *__*:
```
An fhilíocht a chum sí __
the poetry aL composed she
‘the poetry that she composed’
```

Lastly, any finite clause which contains a *resumptive pronoun* is introduced using the final particle, which is termed **aN** (also typically expressed as 'a', but which can also take tense marking e.g 'ar').
See an example below with the resumptive pronoun *her* referring back to *the girl*:
```
An ghirseach a-r ghoid na síogaí í
the girl aN-[PAST] stole the fairies her
‘the girl that the fairies stole away’
```

## Dialectal Variation of Complementiser Usage
This research ultimately aims to distinguish any dialectal variation within the various regions of Ireland when it comes to complementiser usage. To this end a tool will be built that will recognise the complementiser structure of Irish sentence and perform Part-Of-Speech (POS) tagging for the three kinds of complementisers. A small test dataset of 16 Irish sentences containing these complementisers has been compiled for initial testing purposes, and eventually larger datasets will be sought for proper testing and research implementation.
