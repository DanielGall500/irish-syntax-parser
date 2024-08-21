from data_manager.focloir_interface import get_lexical_items_from_focloir

UNIQUE_IRISH_NUMS = [
    "aon",   # 1
    "dó",    # 2
    "trí",   # 3
    "ceathair",  # 4
    "cúig",  # 5
    "sé",    # 6
    "seacht", # 7
    "ocht",  # 8
    "naoi",  # 9
    "deich", # 10
    "fiche", # 20
    "tríocha", # 30
    "daichead", # 40
    "caoga", # 50
    "seasca", # 60
    "seachtó", # 70
    "ochtó", # 80
    "nócha", # 90
    "céad",  # 100
    "míle",  # 1,000
    "milliún"  # 1,000,000
]

IRISH_RESUMPTIVE_PRONOUNS = [
    "leat", "leis", "léi", "linn", "libh", "leo",
    "ort", "air", "uirthi", "orainn", "oraibh", "orthu",
    "agat", "aige", "aici", "againn", "agaibh", "acu",
    "duit", "dó", "di", "dúinn", "daoibh", "dóibh",
    "ionat", "ann", "inti", "ionainn", "ionaibh", "iontu"
]

IRISH_ADJ_PATH = "data/POS/focloir_adjectives.csv"
IRISH_NOUN_PATH = "data/POS/focloir_nouns.csv"
IRISH_ADJECTIVES = get_lexical_items_from_focloir(IRISH_ADJ_PATH)
IRISH_NOUNS = get_lexical_items_from_focloir(IRISH_NOUN_PATH)