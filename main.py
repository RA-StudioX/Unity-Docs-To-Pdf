from pdf_converter import convert_pdfs
from cli_parser import get_cli_args
from topic_utils import print_subtopic_info, get_topic_info

def main():
    args = get_cli_args()
    if args is None:
        return

    if isinstance(args, dict):  # Only proceed if args is a dictionary (i.e., not None and not for list-topics, navigate, or full-tree)
        topic_indices = args['topic_indices']
        depth_limit = args['depth']
        output_pdf = args['output']

        if topic_indices:
            topic_info = get_topic_info()
            selected_topic = topic_info[topic_indices[0]][1]
            print(f"\nSelected topic: {selected_topic}")
            if len(topic_indices) > 1:
                print(f"Selected subtopic indices: {topic_indices[1:]}")
            print("Full path:")
            print_subtopic_info(topic_indices)
        else:
            print("\nConverting all topics")

        if depth_limit:
            print(f"Processing to a depth of {depth_limit}")
        else:
            print("Processing all levels (no depth limit specified)")
        print(f"Output will be saved as: {output_pdf}")

        convert_pdfs(depth_limit=depth_limit, topic_indices=topic_indices, output_pdf=output_pdf)

if __name__ == "__main__":
    main()