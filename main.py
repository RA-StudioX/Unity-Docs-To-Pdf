import sys
import json
import os
from toc_parser import read_toc_structure, parse_json_to_toc_nodes
from pdf_generator import create_toc_pdf

def update_page_numbers(nodes, start_page=1):
    for node in nodes:
        node.update_page_number(start_page)
        start_page += 1
        for child in node.children:
            start_page = update_page_numbers([child], start_page)
    return start_page

def main():
    # Check if a file path was provided as a command-line argument
    if len(sys.argv) < 2:
        print("Please provide the path to the JSON file as a command-line argument.")
        print("Usage: python main.py path/to/your/json_file.json")
        sys.exit(1)
    
    file_path = os.path.abspath(sys.argv[1])
    toc_path = "Manual\\docdata\\toc.json"
    toc_full_path = os.path.join(os.path.abspath(file_path), toc_path)
    print(f"Reading TOC structure from '{toc_full_path}'...")

    try:
        # Read the TOC structure from the JSON file
        toc_json = read_toc_structure(toc_full_path)

        print("TOC structure read successfully.")

        # Convert the JSON to a list of TOCNode instances
        toc_nodes = parse_json_to_toc_nodes(toc_json)

        if not toc_nodes:
            print("Error: Failed to parse the TOC structure. No valid nodes found.")
            sys.exit(1)

        # Update page numbers
        update_page_numbers(toc_nodes)
        
        # Generate PDF
        output_pdf = "table_of_contents.pdf"
        create_toc_pdf(toc_nodes, output_pdf)
        print(f"PDF generated successfully: {output_pdf}")

    except FileNotFoundError:
        print(f"Error: The file '{toc_full_path}' was not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: The file '{toc_full_path}' is not a valid JSON file.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()