from .toc_node import TOCNode
import json

def load_json_toc(json_file):
    """Load the JSON file and return a dictionary."""
    with open(json_file, 'r') as f:
        return json.load(f)

def parse_child_toc(child_data):
    """Parse the child data and return a TOCNode instance."""
    if not isinstance(child_data, dict):
        print(f"Warning: Expected a dictionary, but got {type(child_data)}. Data: {child_data}")
        return None

    title = child_data.get("title")
    link = child_data.get("link")
    children = child_data.get("children", [])

    toc_node = TOCNode(title=title, link=link)
    if not children:
        return toc_node
    
    if not children:
        return toc_node
    
    for child in children:
        child_node = parse_child_toc(child)
        if child_node:
            toc_node.add_child(child_node)
    
    return toc_node

def parse_json_toc(json_file):
    """Parse the JSON file and return a list of dictionaries."""
    toc_json = load_json_toc(json_file)

    if not isinstance(toc_json, dict):
        print(f"Warning: Expected a dictionary, but got {type(toc_json)}. Data: {toc_json}")
        return []
    
    title = toc_json.get("title")
    link = toc_json.get("link")
    children = toc_json.get("children", [])

    toc_node = TOCNode(title=title, link=link)
    for child_data in children:
        child_node = parse_child_toc(child_data)
        if child_node:
            toc_node.add_child(child_node)

    return toc_node

