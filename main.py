import json
from toc_node import TOCNode

def read_toc_structure(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def parse_json_to_toc_node(node_data):
    """
    Recursively converts a JSON structure into a tree of TOCNode instances.
    """
    toc_node = TOCNode(title=node_data["title"], link=node_data.get("link"))

    for child_data in node_data.get('children', []):
        child_node = parse_json_to_toc_node(child_data)
        toc_node.add_child(child_node)

    return toc_node

# Read the TOC structure from the JSON file
toc_json = read_toc_structure('toc_tree.json')

# Convert the JSON to a TOCNode tree structure
toc_root = parse_json_to_toc_node(toc_json)

# Print the tree structure, starting from the children of the root
print(toc_root.get_toc())