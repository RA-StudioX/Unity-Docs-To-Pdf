from pdf_converter import get_topic_info

def print_topic_info():
    topic_info = get_topic_info()
    print("Available topics:")
    for index, title in topic_info:
        print(f"  {index}: {title}")

def get_max_topic_index():
    return len(get_topic_info()) - 1