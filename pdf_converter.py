import pdfkit
import os
from PyPDF2 import PdfMerger
import tempfile
from config import PATH_TO_WKHTMLTOPDF, HTML_DIR, PDF_OPTIONS, OUTPUT_PDF, TOC_DIR
from html_preprocessor import preprocess_html
from TOC import parse_json_toc, TOCNode

pdfkit_config = pdfkit.configuration(wkhtmltopdf=PATH_TO_WKHTMLTOPDF)

def convert_pdfs_recursive(node, temp_dir, current_depth=0, max_depth=None):
    if not node.children or (max_depth is not None and current_depth >= max_depth):
        return []

    for child in node.children:
        convert_pdfs_recursive(child, temp_dir, current_depth + 1, max_depth)

    # Create a PDF for the current node
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

def convert_pdfs(depth_limit=None):
    root_node_list = parse_json_toc(TOC_DIR).children
    # Create a temporary directory to store individual PDFs
    with tempfile.TemporaryDirectory() as temp_dir:

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

        merger.write(OUTPUT_PDF)
        merger.close()

    print(f"\nPDF conversion, ToC generation, and merge complete. Output file: {OUTPUT_PDF}")

def add_content_recursive(node, merger, current_depth=0, max_depth=None):
    if not node.children or (max_depth is not None and current_depth >= max_depth):
        return

    if node.pdf_file and os.path.exists(node.pdf_file):
        merger.append(node.pdf_file)
        print(f"Appending {node.title} to merger")
    else:
        print(f"Warning: PDF file not found or not set for {node.title}")

    for child in node.children:
        add_content_recursive(child, merger, current_depth + 1, max_depth)