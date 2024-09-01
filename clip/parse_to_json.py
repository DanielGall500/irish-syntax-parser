from .tools.syntax.parser import IrishClauseParser
from .data_manager.focloir_interface import FocloirDataInterface
from .preprocessing.string_manipulation import json_path_builder

def main():
    focloir_interface = FocloirDataInterface()
    sentence_parser = IrishClauseParser()

    # -- Step 1: Store the data from each region. --
    datasets = [
        ("go", "Connacht"),
        ("go", "Munster"),
        ("go", "Ulster"),
        ("a", "Connacht"),
        ("a", "Munster"),
        ("a", "Ulster")
    ]
    print("Loading in datasets")
    nrows = 1000

    for dataset in datasets:
        comp = dataset[0]
        region = dataset[1]

        print("DATASET ", comp, region)

        df = focloir_interface.load_dataset(comp, region, nrows)
        sentences = df["sentence"]
        output_path = json_path_builder(comp, region)
        sentence_parser.parse_to(sentences, output_path)

if __name__ == "__main__":
    main()
