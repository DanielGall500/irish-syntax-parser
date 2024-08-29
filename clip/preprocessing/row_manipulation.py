from .tools.morphology.lemmatiser import IrishLemmatiser

lemmatiser = IrishLemmatiser()

def to_lemmas(row):
    main_clause = row['main_clause']
    main_clause_lemmas = lemmatiser(main_clause)

    comp = row['complementiser']
    comp_lemma = lemmatiser(comp)

    embedded_clause = row['embedded_clause']
    embedded_clause_lemmas = lemmatiser(embedded_clause)

    all_lemmas = main_clause_lemmas + comp_lemma + embedded_clause_lemmas
    return { 
        "main": main_clause_lemmas,
        "embedded": embedded_clause_lemmas,
        "comp": comp_lemma,
        "all": all_lemmas
    }
