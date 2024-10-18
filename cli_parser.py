import argparse
from topic_utils import print_topic_info, get_max_topic_index, print_subtopic_info

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Convert Unity Documentation HTML files to PDF with optional file limit.",
        epilog="Example usage: python main.py --topic-index 0 --subtopic-indices 1 2 --depth 2 --output unity_docs.pdf"
    )
    parser.add_argument(
        "--depth", 
        type=int, 
        help="Limit the depth of the topic hierarchy to process. If not specified, all levels will be processed."
    )
    parser.add_argument(
        "--topic-index", 
        type=int, 
        help="Index of the topic to convert (0 to max_index). If not provided, all topics will be converted."
    )
    parser.add_argument(
        "--subtopic-indices",
        nargs='+',
        type=int,
        help="Indices of subtopics to convert. Use space-separated integers to specify the path to the desired subtopic."
    )
    parser.add_argument(
        "--output", 
        type=str, 
        default="output.pdf",
        help="Output PDF file name. Default is 'output.pdf'."
    )
    parser.add_argument(
        "--list-topics", 
        nargs='?',
        const=-1,
        type=int,
        help="List all available topics and their indices, then exit. If an index is provided, list sub-topics for that index."
    )
    return parser.parse_args()

def validate_arguments(args):
    if args.list_topics is not None:
        if args.list_topics == -1:
            print_topic_info()
        else:
            print_subtopic_info(args.list_topics)
        return None

    max_topic_index = get_max_topic_index()

    if args.topic_index is not None:
        if args.topic_index < 0 or args.topic_index > max_topic_index:
            print(f"Error: topic-index must be between 0 and {max_topic_index}")
            print("\nAvailable topics:")
            print_topic_info()
            return None
        topic_indices = [args.topic_index]
    else:
        topic_indices = range(max_topic_index + 1)

    return {
        'topic_indices': topic_indices,
        'subtopic_indices': args.subtopic_indices,
        'depth': args.depth,
        'output': args.output
    }

def get_cli_args():
    args = parse_arguments()
    return validate_arguments(args)