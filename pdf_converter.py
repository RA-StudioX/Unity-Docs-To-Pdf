import pdfkit
import os
from PyPDF2 import PdfMerger
import tempfile
from config import PATH_TO_WKHTMLTOPDF, HTML_DIR, PDF_OPTIONS, TOC_DIR
from html_preprocessor import preprocess_html
from TOC import parse_json_toc, TOCNode
from PyPDF2.generic import Destination, Fit

pdfkit_config = pdfkit.configuration(wkhtmltopdf=PATH_TO_WKHTMLTOPDF)

def convert_pdfs_recursive(node, temp_dir, current_depth=0, max_depth=None):
    if node is None or (max_depth is not None and current_depth > max_depth):
        return

    # Convert the current node to PDF
    pdf_file = os.path.join(temp_dir, f"{node.title}.pdf")
    html_path = os.path.join(HTML_DIR, f"{node.link}.html")
    
    try:
        # Read the HTML content
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Preprocess the HTML content
        base_path = os.path.dirname(html_path)
        preprocessed_html = preprocess_html(html_content, base_path)
        
        # Pass the preprocessed HTML directly to pdfkit
        pdfkit.from_string(preprocessed_html, pdf_file, configuration=pdfkit_config, options=PDF_OPTIONS)
        node.add_pdf_file(pdf_file)
        print(f"Converted {node.title} to PDF")
    except Exception as e:
        print(f"Error converting {node.title}: {str(e)}")

    # Process children
    for child in node.children:
        convert_pdfs_recursive(child, temp_dir, current_depth + 1, max_depth)

def find_topic_node(root_node, topic_indices):
    if not topic_indices:
        return None

    current_node = root_node
    for index in topic_indices:
        if 0 <= index < len(current_node.children):
            current_node = current_node.children[index]
        else:
            return None
    return current_node

def convert_pdfs(output_pdf, depth_limit=None, topic_indices=None):
    root_node = parse_json_toc(TOC_DIR)
    
    # Create a temporary directory to store individual PDFs
    with tempfile.TemporaryDirectory() as temp_dir:
        if topic_indices and len(topic_indices) < len(root_node.children):
            selected_node = find_topic_node(root_node, topic_indices)
            if selected_node:
                print(f"\nConverting from topic: {selected_node.title}")
                convert_pdfs_recursive(selected_node, temp_dir, max_depth=depth_limit)
            else:
                print(f"Error: Invalid topic indices.")
                return
        else:
            print("\nConverting all topics")
            for node in root_node.children:
                convert_pdfs_recursive(node, temp_dir, max_depth=depth_limit)

        print("\nAll individual PDFs created. Merging...")

        # Step 2: Generate ToC and merge PDFs
        merger = PdfMerger()

        # Add content pages
        if topic_indices and len(topic_indices) < len(root_node.children):
            selected_node = find_topic_node(root_node, topic_indices)
            if selected_node:
                add_content_recursive(selected_node, merger, max_depth=depth_limit)
        else:
            for node in root_node.children:
                add_content_recursive(node, merger, max_depth=depth_limit)

        merger.write(output_pdf)
        merger.close()

    print(f"\nPDF conversion, ToC generation, and merge complete. Output file: {output_pdf}")

def add_content_recursive(node, merger, current_depth=0, max_depth=None, parent_bookmark=None):
    if node is None or (max_depth is not None and current_depth > max_depth):
        return

    if node.pdf_file and os.path.exists(node.pdf_file):
        # Get the current page count before appending
        start_page = len(merger.pages)
        
        # Append the PDF
        merger.append(node.pdf_file, import_outline=False)
        print(f"Appending {node.title} to merger")

        # Create a bookmark for this node
        bookmark = merger.add_outline_item(
            node.link,
            page_number=start_page,
            parent=parent_bookmark
        )

    else:
        print(f"Warning: PDF file not found or not set for {node.link}")
        bookmark = parent_bookmark

    # Recursively process children
    for child in node.children:
        add_content_recursive(child, merger, current_depth + 1, max_depth, bookmark)