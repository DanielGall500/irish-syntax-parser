from .tools.syntax.parser import ParsedSentence
from .mccloskey_parser import McCloskeyParser
from .preprocessing.string_manipulation import json_path_builder
from collections import Counter
import plotly.graph_objects as go
import json

class EmbeddingCounter:
    def __init__(self):
        pass

    def __call__(self, sentences: list[ParsedSentence]) -> dict:
        embeddings = {}
        embedding_key = lambda i, src, tgt: ("E{}-{}".format(i+1, src), "E{}-{}".format(i+2, tgt))
        for s in sentences:
            n_clauses = s.get_num_clauses()
            for i,c in enumerate(s):
                comp = c["selected_comp"]
                if i+1 < n_clauses:
                    comp_2 = s[i+1]["selected_comp"]
                else:
                    comp_2 = "T"

                if not comp:
                    break

                key = embedding_key(i, comp, comp_2)

                if not key in embeddings.keys():
                    embeddings[key] = 1
                else:
                    embeddings[key] += 1

        """
        for k in embeddings.keys():
            comps_at_embedding_X = embeddings[k]
            counted = dict(Counter(comps_at_embedding_X).most_common())
            embeddings[k] = counted
        """
        return embeddings

def main():
    embedding_counter = EmbeddingCounter()
    sentence_parser = McCloskeyParser()

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

    for dataset in datasets:
        comp = dataset[0]
        region = dataset[1]

        print("DATASET ", comp, region)
        path = json_path_builder(comp, region)
        parsed_sentences = sentence_parser.parse_from_json(path)
        embeddings = embedding_counter(parsed_sentences)
        # print(json.dumps(embeddings, indent=4))

        node_labels = set()
        for (src, tgt) in embeddings.keys():
            if src is not None:
                node_labels.add(src)
            if tgt is not None:
                node_labels.add(tgt)

        node_labels = sorted(node_labels)  # Sort to have consistent indexing
        node_map = {label: i for i, label in enumerate(node_labels)}

        sources = [node_map[x] for (x,y) in embeddings.keys()]
        targets = [node_map[y] for (x,y) in embeddings.keys()]
        values = list(embeddings.values())

        print(node_labels)
        print(sources)
        print(targets)
        print(values)
        # Create the Sankey diagram
        diagram_labels = [x[3:] for x in node_labels]
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=diagram_labels,
            ),
            link=dict(
                source=sources,  # indices of source nodes
                target=targets,  # indices of target nodes
                value=values,    # flow values
            )
        )])

        # Set the title and layout
        fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)

        # Display the Sankey diagram
        fig.show()


if __name__ == "__main__":
    main()

