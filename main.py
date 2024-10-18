from pdf_converter import convert_pdfs
from cli_parser import get_cli_args
from topic_utils import print_subtopic_info, get_topic_info, find_topic_node
from TOC import parse_json_toc
from config import TOC_DIR

def main():
    args = get_cli_args()
    if args is None:
        return

    if isinstance(args, dict):  # Only proceed if args is a dictionary
        topic_indices = args['topic_indices']
        depth_limit = args['depth']
        output_pdf = args['output']

        root_node = parse_json_toc(TOC_DIR)

        print(f"Debug: Topic indices: {topic_indices}")  # Debug print

        topic_info = get_topic_info()
        if len(topic_indices) == len(topic_info):
            print("\nConverting all topics")
        elif topic_indices:
            if topic_indices[0] < 0 or topic_indices[0] >= len(topic_info):
                print(f"Error: Invalid first topic index. Must be between 0 and {len(topic_info) - 1}")
                return

            selected_topic = topic_info[topic_indices[0]][1]
            print(f"\nSelected topic: {selected_topic}")
            if len(topic_indices) > 1:
                print(f"Selected subtopic indices: {topic_indices[1:]}")
            print("Full path:")
            try:
                print_subtopic_info(topic_indices)
            except IndexError:
                print("Error: Invalid subtopic index.")
                return

            # Validate the entire topic path
            selected_node = find_topic_node(root_node, topic_indices)
            if selected_node is None:
                print("Error: Invalid topic path. Please check your topic indices.")
                return
        else:
            print("\nNo specific topic path provided. Converting all topics.")

        if depth_limit:
            print(f"Processing to a depth of {depth_limit}")
        else:
            print("Processing all levels (no depth limit specified)")
        print(f"Output will be saved as: {output_pdf}")

        convert_pdfs(output_pdf, depth_limit=depth_limit, topic_indices=topic_indices)

if __name__ == "__main__":
    main()