from ..language.syntax import EOS_CHARS
import os

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

def remove_eos_characters(T: str) -> str:
    no_eos_characters = ''.join([char for char in T if char not in EOS_CHARS])
    return no_eos_characters

folder_basic_parsing = "data/complementiser_parsed"
folder_mccloskey_parsing = "data/mccloskey_parsed"
dataset_title_template = "parsed_dataset_"
path_builder = lambda folder, file: os.path.join(folder, file)
json_path_builder = lambda comp, region: path_builder(folder_basic_parsing, dataset_title_template + comp + "_" + region + ".json")
csv_path_builder = lambda comp, region: path_builder(folder_mccloskey_parsing, dataset_title_template + comp + "_" + region + ".csv")