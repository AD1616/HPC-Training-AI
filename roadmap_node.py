from __future__ import annotations
import json


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

    def to_dict(self) -> dict[str, any]:
        return {
            "name": self.name,
            "prompt": self.prompt,
            "children": [child.to_dict() for child in self.children]
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=4)


if __name__ == "__main__":
    test_third = RoadmapNode(name="Third", prompt="Third", children=[])
    test_child = RoadmapNode(name="Test Child", prompt="Child Prompt", children=[test_third])
    test_root = RoadmapNode(name="Test Root", prompt="Root Prompt", children=[test_child])

    print(json.dumps(test_root.to_dict()))
