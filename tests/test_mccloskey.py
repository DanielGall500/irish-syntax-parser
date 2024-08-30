from clip import IrishClauseParser
import pandas as pd
import unittest

class TestExample(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        mccloskey_data_path = "data/mccloskey-complementiser-data.csv"
        mccloskey_data = pd.read_csv(mccloskey_data_path, header=0)

        irish_sentences = list(mccloskey_data['sentence_irish'])
        english_translations = list(mccloskey_data['sentence_english'])

        sentence_parser = IrishClauseParser()
        cls.parsed_sentences = []

        for sentence in irish_sentences:
            parsed_s = sentence_parser.parse_to_dict(sentence)
            cls.parsed_sentences.append(parsed_s)

    def setUp(self):
        """Runs before every test method."""
        self.test_resource = "This is a test resource"
        print("Setup method")

    def test_example1(self):
        """A sample test."""
        print("Running test_example1")
        sentence_example = self.parsed_sentences[0]
        self.assertEqual(sentence_example["num_clauses"], 2)

    def tearDown(self):
        """Runs after every test method."""
        print("Winding down the test.")
        print("Teardown method")

    @classmethod
    def tearDownClass(cls):
        """Runs once for the entire test class."""
        print("Teardown class")

if __name__ == "__main__":
    unittest.main()