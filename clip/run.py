from .tools.syntax.parser import IrishClauseParser, ParsedSentence
from .mccloskey_parser import McCloskeyParser
from .preprocessing.string_manipulation import json_path_builder, csv_path_builder
import pandas as pd
from collections import deque, Counter

class ExperimentBase:
    def setup(self):
        pass

    def run(self):
        raise NotImplementedError("Subclasses should implement this!")

    def teardown(self):
        pass

    def execute(self):
        self.setup()
        result = self.run()
        self.teardown()
        return result

class AnalyseNounBeforeGoExperiment(ExperimentBase):
    def __init__(self, sentences):
        self.sentences = sentences

    def setup(self):
        self.nouns_before_comp_counter = 0
        self.total_clauses_counter = 0

    def run(self):
        for sentence in self.sentences:
            for clause in sentence:
                if clause["noun_final"]:
                    self.nouns_before_comp_counter += 1
                self.total_clauses_counter += 1

        percentage = (self.nouns_before_comp_counter / self.total_clauses_counter) * 100 if self.total_clauses_counter > 0 else 0

        return {
            "Number of complementisers preceded by noun": self.nouns_before_comp_counter,
            "Number of clauses": self.total_clauses_counter,
            "Percentage": percentage
        }

class AnalyseAExperiment(ExperimentBase):
    def __init__(self, sentences):
        self.sentences = sentences

    def setup(self):
        self.res_pronoun_counter = 0
        self.n_sentences = len(self.sentences)

    def run(self):
        for sentence in self.sentences:
            n_clauses = sentence.get_num_clauses()
            if n_clauses > 1:
                final_clause = deque(sentence, maxlen=1)[0]
                if final_clause.get("is_resumptive_found", False):
                    self.res_pronoun_counter += 1

        percentage = (self.res_pronoun_counter / self.n_sentences) * 100 if self.n_sentences > 0 else 0

        return {
            "Number of resumptive final comps found": self.res_pronoun_counter,
            "Number of sentences": self.n_sentences,
            "Percentage": percentage
        }

class McCloskeyParserExperiment(ExperimentBase):
    def __init__(self, sentences, output_path=None):
        self.sentences = sentences
        self.output_path = output_path

    def setup(self):
        self.parser = McCloskeyParser()

    def run(self):
        parsed_sentences = self.parser.parse_to_list(self.sentences)
        counted_ps = dict(Counter(parsed_sentences).most_common())
        patterns = counted_ps.keys()
        occurrences = counted_ps.values()

        df = pd.DataFrame({
            "pattern": patterns,
            "count": occurrences
        })
        self.output_df = df

        return dict(counted_ps)

    def teardown(self):
        # save the results to their own CSV file
        self.output_df.to_csv(self.output_path, index=False)
        pass

class ExperimentRunner:
    def __init__(self, experiments):
        self.experiments = experiments

    def run_all(self):
        results = {}
        for experiment in self.experiments:
            print(f"Running {experiment.__class__.__name__}")
            result = experiment.execute()
            results[experiment.__class__.__name__] = result
        return results

def main():
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
    for dataset in datasets:
        comp = dataset[0]
        region = dataset[1]
        path = json_path_builder(comp, region)
        parsed_sentences = sentence_parser.read_from(path)
        parsed_sentences = [ParsedSentence(sentence) for sentence in parsed_sentences]
        output_path = csv_path_builder(comp, region)

        print("\n\n")
        print("Dataset: {}, {}".format(comp, region))
        if comp == "go":
            experiments = [
                AnalyseNounBeforeGoExperiment(parsed_sentences),
                McCloskeyParserExperiment(parsed_sentences, output_path)
            ]
        elif comp == "a":
            experiments = [
                AnalyseAExperiment(parsed_sentences),
                McCloskeyParserExperiment(parsed_sentences, output_path)
            ]
        else:
            print("Invalid complementiser.")
            continue

        runner = ExperimentRunner(experiments)
        results = runner.run_all()

        for name, result in results.items():
            print(f"{name}:")
            for key, value in result.items():
                print(f"  {key}: {value}")
    
if __name__ == "__main__":
    main()