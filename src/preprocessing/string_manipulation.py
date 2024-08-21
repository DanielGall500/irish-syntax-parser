from language.syntax import EOS_CHARS

def up_to_end_of_sentence(T: str) -> str:
    final_string = ""
    for c in T:
        if c not in EOS_CHARS:
            final_string += c
        else:
            break
    return final_string

def from_beginning_of_sentence(T: str) -> str:
    final_string = ""
    i = len(T)-1
    while i >= 0:
        if T[i] in EOS_CHARS:
            break
        final_string += T[i]
        i -= 1
    return final_string[::-1]