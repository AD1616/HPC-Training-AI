from generate_topics import topics
from query import generate_output
# from roadmaps.roadmap_node import RoadmapNode


def generate(query):
    related_docs = generate_output(query)[1]
    # children_data = topics(related_docs, query)

    # children = []
    # for child in children_data:
    #     children.append(RoadmapNode(name=child[0], prompt=child[1], children=[]))
    # root = RoadmapNode(name="Your Query", prompt=query, children=children)
    #
    # return root


if __name__ == "__main__":
    # test_root = generate("Parallel computing")
    # test_root_json = test_root.to_json()
    #
    # print(test_root_json)

    generate("parallel computing")