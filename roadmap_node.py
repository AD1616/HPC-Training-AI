from __future__ import annotations


class RoadmapNode:
    name: str
    prompt: str
    children: list[RoadmapNode]

    def __init__(self, name: str, prompt: str, children: list[RoadmapNode]):
        self.name = name
        self.prompt = prompt
        self.children = children

    def __str__(self) -> str:
        return f"{self.name} | {self.prompt}"

    def get_children(self) -> str:
        output = ""
        for child in self.children:
            output += child.__str__()

        return output


if __name__ == "__main__":
    test_child = RoadmapNode(name="Test Child", prompt="Child Prompt", children=[])
    test_root = RoadmapNode(name="Test Root", prompt="Root Prompt", children=[test_child])

    print("Root: " + test_root.__str__())
    print("Child: " + test_child.__str__())
    print("Root's Child: " + test_root.get_children())

