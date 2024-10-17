import json
from toc_node import TOCNode

def read_toc_structure(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def parse_json_to_toc_nodes(node_data):
    """
    Converts a JSON structure into a list of TOCNode instances, ignoring the root.
    """
    if not isinstance(node_data, dict):
        print(f"Warning: Expected a dictionary, but got {type(node_data)}. Data: {node_data}")
        return []

    children = node_data.get('children', [])
    if not isinstance(children, list):
        print(f"Warning: 'children' is not a list. Type: {type(children)}. Node data: {node_data}")
        return []

    toc_nodes = []
    for child_data in children:
        child_node = parse_json_to_toc_node(child_data)
        if child_node:
            toc_nodes.append(child_node)

    return toc_nodes

def parse_json_to_toc_node(node_data):
    """
    Recursively converts a JSON structure into a TOCNode instance.
    """
    if not isinstance(node_data, dict):
        print(f"Warning: Expected a dictionary, but got {type(node_data)}. Data: {node_data}")
        return None

    title = node_data.get("title")
    link = node_data.get("link")
    
    if title is None:
        print(f"Warning: Node is missing 'title'. Node data: {node_data}")
        return None

    toc_node = TOCNode(title=title, link=link)

    children = node_data.get('children', [])
    if isinstance(children, list):
        for child_data in children:
            child_node = parse_json_to_toc_node(child_data)
            if child_node:
                toc_node.add_child(child_node)
    elif children is not None:
        print(f"Warning: 'children' is not a list. Type: {type(children)}. Node data: {node_data}")

    return toc_node