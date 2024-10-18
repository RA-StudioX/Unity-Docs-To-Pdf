import pdfkit
import os
from PyPDF2 import PdfMerger
import tempfile
from config import PATH_TO_WKHTMLTOPDF, HTML_DIR, PDF_OPTIONS, TOC_OPTIONS, OUTPUT_PDF

pdfkit_config = pdfkit.configuration(wkhtmltopdf=PATH_TO_WKHTMLTOPDF)

def convert_pdfs(file_limit=None):
    # Create a temporary directory to store individual PDFs
    with tempfile.TemporaryDirectory() as temp_dir:
        # Step 1: Convert each HTML file to a PDF
        html_files = [f for f in os.listdir(HTML_DIR) if f.endswith('.html')]
        
        if file_limit:
            html_files = html_files[:file_limit]
        
        pdf_files = []
        total_files = len(html_files)

        for index, html_file in enumerate(html_files, start=1):
            pdf_file = os.path.join(temp_dir, html_file.replace('.html', '.pdf'))
            html_path = os.path.join(HTML_DIR, html_file)
            
            # Change the current working directory to the HTML file's directory
            original_cwd = os.getcwd()
            os.chdir(os.path.dirname(html_path))
            
            try:
                # Pass the options to pdfkit.from_file
                pdfkit.from_file(html_file, pdf_file, configuration=pdfkit_config, options=PDF_OPTIONS)
                pdf_files.append(pdf_file)

                # Notify after each PDF is created
                print(f"Converted {index}/{total_files}: {html_file} to PDF")
            except Exception as e:
                print(f"Error converting {html_file}: {str(e)}")
            finally:
                # Change back to the original working directory
                os.chdir(original_cwd)

        print("\nAll individual PDFs created. Generating Table of Contents and merging...")

        # Step 2: Generate ToC and merge PDFs
        merger = PdfMerger()

        # Add cover page if exists
        if os.path.exists('cover.pdf'):
            merger.append('cover.pdf')

        # Add content pages
        for pdf_file in pdf_files:
            merger.append(pdf_file)

        merger.write(OUTPUT_PDF)
        merger.close()

    print(f"\nPDF conversion, ToC generation, and merge complete. Output file: {OUTPUT_PDF}")