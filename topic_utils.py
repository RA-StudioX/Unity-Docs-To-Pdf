from TOC import parse_json_toc, TOCNode
from config import TOC_DIR

def print_topic_info():
    topic_info = get_topic_info()
    print("Available topics:")
    for index, title in topic_info:
        print(f"  {index}: {title}")

def get_max_topic_index():
    return len(get_topic_info()) - 1

def get_topic_info():
    root_node = parse_json_toc(TOC_DIR)
    return [(i, child.title) for i, child in enumerate(root_node.children)]

def print_subtopic_info(topic_indices):
    root_node = parse_json_toc(TOC_DIR)
    current_node = root_node

    # Navigate to the specified node
    for index in topic_indices:
        if 0 <= index < len(current_node.children):
            current_node = current_node.children[index]
        else:
            print(f"Error: Invalid topic index {index}.")
            return

    print(f"Sub-topics for '{current_node.title}':")
    print_subtopics_recursive(current_node)

def print_subtopics_recursive(node, prefix="", path=[]):
    for index, child in enumerate(node.children):
        current_path = path + [index]
        path_str = ' '.join(map(str, current_path))
        print(f"{prefix}- [{path_str}] {child.title}")
        if child.children:
            print_subtopics_recursive(child, prefix + "  ", current_path)

def navigate_topics(topic_indices=None):
    root_node = parse_json_toc(TOC_DIR)
    current_node = root_node

    while True:
        if topic_indices:
            for index in topic_indices:
                if 0 <= index < len(current_node.children):
                    current_node = current_node.children[index]
                else:
                    print(f"Error: Invalid topic index {index}.")
                    return
            topic_indices = None
        
        print(f"\nCurrent topic: {current_node.title}")
        print_subtopics_recursive(current_node)
        
        user_input = input("\nEnter subtopic index to navigate (space-separated for multiple levels), 'b' to go back, or 'q' to quit: ").strip().lower()
        
        if user_input == 'q':
            break
        elif user_input == 'b':
            if current_node == root_node:
                print("Already at the root level.")
            else:
                current_node = root_node  # Reset to root
        else:
            try:
                indices = list(map(int, user_input.split()))
                topic_indices = indices
            except ValueError:
                print("Invalid input. Please enter space-separated integers, 'b', or 'q'.")

def print_full_topic_tree():
    root_node = parse_json_toc(TOC_DIR)
    print("Full topic tree:")
    for index, child in enumerate(root_node.children):
        print(f"{index}: {child.title}")
        print_subtopics_recursive(child, "  ", [index])

def get_topic_info():
    root_node = parse_json_toc(TOC_DIR)
    return [(i, child.title) for i, child in enumerate(root_node.children)]

def get_max_topic_index():
    return len(get_topic_info()) - 1

def find_topic_node(root_node, topic_indices):
    current_node = root_node
    for index in topic_indices:
        if 0 <= index < len(current_node.children):
            current_node = current_node.children[index]
        else:
            return None
    return current_node