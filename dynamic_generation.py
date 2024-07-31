from query import generate_output
from generate_topics import topics
from roadmaps.roadmap_node import RoadmapNode


def generate(query):
    related_docs = generate_output(query)[1]
    children_data = topics(documents=related_docs, question=query)

    children = []
    for child in children_data:
        children.append(RoadmapNode(name=child[0], prompt=child[1], children=[]))
    root = RoadmapNode(name=query, prompt=query, children=children)

    return root


def generate_tree(query: str, level: int, visited: set):
    children = []
    if level > 1:
        return children

    children_data = get_topics_and_queries(query)
    for child in children_data:
        if child[0] in visited:
            continue
        visited.add(child[0])
        child_children = generate_tree(child[1], level + 1, visited)
        children.append(RoadmapNode(name=child[0], prompt=child[1], children=child_children))

    return children


def get_topics_and_queries(query: str):
    related_docs = generate_output(query)[1]
    children_data = topics(documents=related_docs, question=query)

    return children_data


if __name__ == "__main__":
    test_root = RoadmapNode(name="Parallel Computing Roadmap", prompt="Parallel Computing", children=generate_tree("Parallel Computing", 0, set()))
    test_root_json = test_root.to_json()
    with open("roadmaps/dynamic_generation_test.json", "w") as outfile:
        outfile.write(test_root_json)

    print(test_root_json)
