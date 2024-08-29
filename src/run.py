from tools.syntax.parser import SentenceParser, ParsedSentence
from preprocessing.string_manipulation import json_path_builder
from collections import deque

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

    def run(self):
        nouns_before_comp_counter = 0
        total_clauses_counter = 0
        for sentence in self.sentences:
            for clause in sentence:
                if clause["noun_final"]:
                    nouns_before_comp_counter += 1
                total_clauses_counter += 1

        percentage = (nouns_before_comp_counter / total_clauses_counter) * 100 if total_clauses_counter > 0 else 0

        return {
            "Number of complementisers preceded by noun": nouns_before_comp_counter,
            "Number of clauses": total_clauses_counter,
            "Percentage": percentage
        }

class AnalyseAExperiment(ExperimentBase):
    def __init__(self, sentences):
        self.sentences = sentences

    def run(self):
        res_pronoun_counter = 0
        n_sentences = len(self.sentences)

        for sentence in self.sentences:
            n_clauses = sentence.get_num_clauses()
            if n_clauses > 1:
                final_clause = deque(sentence, maxlen=1)[0]
                if final_clause.get("is_resumptive_found", False):
                    res_pronoun_counter += 1

        percentage = (res_pronoun_counter / n_sentences) * 100 if n_sentences > 0 else 0

        return {
            "Number of resumptive final comps found": res_pronoun_counter,
            "Number of sentences": n_sentences,
            "Percentage": percentage
        }

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
    sentence_parser = SentenceParser()

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

        print("Dataset: {}, {}".format(comp, region))
        if comp == "go":
            experiments = [
                AnalyseNounBeforeGoExperiment(parsed_sentences),
            ]
        elif comp == "a":
            experiments = [
                AnalyseAExperiment(parsed_sentences),
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