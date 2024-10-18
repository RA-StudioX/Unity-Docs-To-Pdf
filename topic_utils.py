from pdf_converter import get_topic_info
from TOC import parse_json_toc, TOCNode
from config import TOC_DIR

def print_topic_info():
    topic_info = get_topic_info()
    print("Available topics:")
    for index, title in topic_info:
        print(f"  {index}: {title}")

def get_max_topic_index():
    return len(get_topic_info()) - 1

def print_subtopic_info(topic_index, depth=None, prefix=""):
    root_node = parse_json_toc(TOC_DIR)
    if 0 <= topic_index < len(root_node.children):
        topic_node = root_node.children[topic_index]
        print(f"Sub-topics for '{topic_node.title}':")
        print_subtopics_recursive(topic_node, depth, prefix)
    else:
        print(f"Error: Invalid topic index. Please choose a number between 0 and {len(root_node.children) - 1}")

def print_subtopics_recursive(node, depth=None, prefix="", current_depth=0):
    if depth is not None and current_depth >= depth:
        return

    print(f"{prefix}- {node.title}")
    
    for child in node.children:
        print_subtopics_recursive(child, depth, prefix + "  ", current_depth + 1)