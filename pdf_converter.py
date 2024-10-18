import pdfkit
import os
from PyPDF2 import PdfMerger
import tempfile
from config import PATH_TO_WKHTMLTOPDF, HTML_DIR, PDF_OPTIONS, TOC_DIR
from html_preprocessor import preprocess_html
from TOC import parse_json_toc, TOCNode

pdfkit_config = pdfkit.configuration(wkhtmltopdf=PATH_TO_WKHTMLTOPDF)

def get_topic_info():
    root_node = parse_json_toc(TOC_DIR)
    return [(i, child.title) for i, child in enumerate(root_node.children)]

def get_max_topic_index():
    return len(get_topic_info()) - 1

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

def convert_pdfs(output_pdf, depth_limit=None, topic_index=None):
    root_node = parse_json_toc(TOC_DIR)
    root_node_list = root_node.children
    # Create a temporary directory to store individual PDFs
    with tempfile.TemporaryDirectory() as temp_dir:
        root_node_list = root_node_list[topic_index:topic_index+1] if topic_index is not None else root_node_list
        for node in root_node_list:
            convert_pdfs_recursive(node, temp_dir, max_depth=depth_limit)

        print("\nAll individual PDFs created. Merging...")

        # Step 2: Generate ToC and merge PDFs
        merger = PdfMerger()

        # Add cover page if exists
        if os.path.exists('cover.pdf'):
            merger.append('cover.pdf')

        # Add content pages
        for node in root_node_list:
            add_content_recursive(node, merger, max_depth=depth_limit)

        merger.write(output_pdf)
        merger.close()

    print(f"\nPDF conversion, ToC generation, and merge complete. Output file: {output_pdf}")

def add_content_recursive(node, merger, current_depth=0, max_depth=None):
    if node is None or (max_depth is not None and current_depth > max_depth):
        return

    if node.pdf_file and os.path.exists(node.pdf_file):
        merger.append(node.pdf_file)
        print(f"Appending {node.title} to merger")
    else:
        print(f"Warning: PDF file not found or not set for {node.title}")

    for child in node.children:
        add_content_recursive(child, merger, current_depth + 1, max_depth)