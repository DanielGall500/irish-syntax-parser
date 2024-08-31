# CLIP: Clause-based Irish Parser
## Recursively parse Irish into its clauses with encoded linguistic features.

Irish is a highly inflectional Celtic language with Verb-Subject-Object (VSO) word order. In this research we will examine the Irish complementisers and their unique properties when it comes to long-distance dependencies, such as in the sentence *"He’s the guy that they said they thought they wanted to hire __"*, where long-distance movement has taken place from the original position of "the guy" after "hire". Irish has two strategies in order to model this type of long-distance dependency:
1. Movement takes place as in the example above and you are left with a trace (unfilled space).
2. Use a resumptive pronoun which provides an indication back to what is being referred to. Resumptive pronouns are not typical in English, but can still be expressed. For instance, in the sentence "This is the girl that whenever it rains she cries." Here, "she" acts as the resumptive pronoun, restating the person on whom an action is being completed.

## Forms of Irish Complementisers
### Go Particle
We begin with finite complement clauses, which is the simplest case where there are no long-distance dependencies. This complementiser particle will typically be preceded by a verb (He said that...) or adjective (I am sure that...). The particle used here is termed the **go** particle, which can surface in various ways due to it taking tense marking. For instance, in the following example the *go* particle takes a past-tense marking *r*:
```
Creidim gu-r inis sé bréag. 
I-believe go–[PAST] tell he lie 
‘I believe that he told a lie.’
```
The forms of this particle are "go", "gur" (past / conditional form when followed by a consonant), "gurb" (present / future form before a vowel) , and "gurbh" (past / conditional form when followed by a vowel). The use of this particle triggers lenition.

### aL Particle
Any finite clause which contains a trace due to non-local movement is introduced using a different particle, one which is termed **aL** (expressed as 'a').
We can see an example of this below with a trace *__*:
```
An fhilíocht a chum sí __
the poetry aL composed she
‘the poetry that she composed’
```

### aN Particle
Lastly, any finite clause which contains a *resumptive pronoun* is introduced using the final particle, which is termed **aN** (also typically expressed as 'a', but which can also take tense marking e.g 'ar').
See an example below with the resumptive pronoun *her* referring back to *the girl*:
```
An ghirseach a-r ghoid na síogaí í
the girl aN-[PAST] stole the fairies her
‘the girl that the fairies stole away’
```

## Dialectal Variation of Complementiser Usage
This research ultimately aims to distinguish any dialectal variation within the various regions of Ireland when it comes to complementiser usage. To this end a tool will be built that will recognise the complementiser structure of Irish sentence and perform Part-Of-Speech (POS) tagging for the three kinds of complementisers. A small test dataset of 16 Irish sentences containing these complementisers has been compiled for initial testing purposes, and eventually larger datasets will be sought for proper testing and research implementation.

Certainly! Here’s a template for a `README.md` file tailored for your Python package that parses Irish sentences into their clauses. This README includes sections on installation, usage, contributing, and license information.

---

## Features

- **Parse Irish Sentences**: Converts full Irish sentences into individual clauses.
- **Clause Analysis**: Provides tools for analyzing clauses based on various linguistic features.
- **Extensible**: Easy to extend with additional parsing rules or features.

## Installation
To install the `clip-irish` package, you can use pip. Ensure that you have Python 3.9 or later installed on your system.

```bash
pip install clip-irish
```

Or, if you're developing the package locally:

```bash
pip install -e .
```

## Usage
Here’s a basic example of how to use the `clip-irish` package to parse Irish sentences:

```python
from clip.parse import IrishClauseParser

# Create a parser instance
parser = IrishClauseParser()

# Example Irish sentence from McCloskey
sentence = "Creidim gur inis sé bréag."

# Parse the sentence
parsed_clauses = parser(sentence)

# Print parsed clauses
for c in parsed_clauses:
    print(c["clause"])
```

### Available Methods
### Examples
** TODO

## Testing
To run tests for the package, use the following command:

```bash
python -m unittest
```

Tests are located in the `tests` directory and are automatically run in CI/CD pipelines to ensure code quality.

## Contributing

Contributions are welcome! To contribute to this project, follow these steps:

1. **Fork the repository** on GitHub.
2. **Create a new branch** for your feature or bug fix.
3. **Make your changes** and ensure that all tests pass.
4. **Submit a pull request** with a clear description of your changes.

Please make sure to follow the code style and write tests for new features.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, please contact [Daniel Gallagher](mailto:daniel.gallagher.js@gmail.com).

---
