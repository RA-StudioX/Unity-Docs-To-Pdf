from pdf_converter import convert_pdfs, get_topic_info
from cli_parser import get_cli_args

def main():
    args = get_cli_args()
    if args is None:
        return

    topic_indices = args['topic_indices']
    depth_limit = args['depth']
    output_pdf = args['output']

    if len(topic_indices) == 1:
        topic_info = get_topic_info()
        selected_topic = topic_info[topic_indices[0]][1]
        print(f"\nConverting topic: {selected_topic}")
    else:
        print("\nConverting all topics")

    if depth_limit:
        print(f"Processing to a depth of {depth_limit}")
    else:
        print("Processing all levels (no depth limit specified)")
    print(f"Output will be saved as: {output_pdf}")

    for index in topic_indices:
        if len(topic_indices) > 1:
            topic_info = get_topic_info()
            current_topic = topic_info[index][1]
            print(f"\nConverting topic {index}: {current_topic}")
        convert_pdfs(depth_limit=depth_limit, topic_index=index, output_pdf=output_pdf)

    if len(topic_indices) > 1:
        print(f"\nAll topics have been converted and saved to {output_pdf}")

if __name__ == "__main__":
    main()