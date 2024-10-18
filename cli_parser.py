import argparse
from topic_utils import print_topic_info, get_max_topic_index, print_subtopic_info, print_full_topic_tree

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Convert Unity Documentation HTML files to PDF with optional file limit.",
        epilog="Example usage: python main.py --topic-path 0/1/2 --depth 2 --output unity_docs.pdf"
    )
    parser.add_argument(
        "--depth", 
        type=int, 
        help="Limit the depth of the topic hierarchy to process. If not specified, all levels will be processed."
    )
    parser.add_argument(
        "--topic-path", 
        type=str,
        help="Path to the topic to convert. Use slash-separated integers to specify the path to the desired topic/subtopic. Example: '0/1/2'"
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
        const='all',
        help="List topics and subtopics. Use slash-separated integers to specify the path to the desired topic/subtopic, or 'all' to list main topics. Example: '0/1/2'"
    )
    parser.add_argument(
        "--full-tree",
        action="store_true",
        help="Print the full topic tree with all subtopics and their indices."
    )
    return parser.parse_args()

def validate_arguments(args):
    if args.list_topics is not None:
        if args.list_topics == 'all':
            print_topic_info()
        else:
            try:
                topic_indices = [int(i) for i in args.list_topics.split('/')]
                print_subtopic_info(topic_indices)
            except ValueError:
                print(f"Error: Invalid topic path '{args.list_topics}'. Please provide integers separated by '/'.")
        return None
    
    if args.full_tree:
        print_full_topic_tree()
        return None

    max_topic_index = get_max_topic_index()

    if args.topic_path:
        topic_indices = [int(i) for i in args.topic_path.split('/')]
        if topic_indices[0] < 0 or topic_indices[0] > max_topic_index:
            print(f"Error: First topic index must be between 0 and {max_topic_index}")
            print("\nAvailable topics:")
            print_topic_info()
            return None
    else:
        topic_indices = list(range(max_topic_index + 1))

    return {
        'topic_indices': topic_indices,
        'depth': args.depth,
        'output': args.output
    }

def get_cli_args():
    args = parse_arguments()
    return validate_arguments(args)