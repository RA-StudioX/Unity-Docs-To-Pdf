import pdfkit
import os
import subprocess
import tempfile
from config import PATH_TO_WKHTMLTOPDF, HTML_DIR, PDF_OPTIONS, OUTPUT_PDF
from html_preprocessor import preprocess_html

pdfkit_config = pdfkit.configuration(wkhtmltopdf=PATH_TO_WKHTMLTOPDF)

def convert_pdfs(file_limit=None):
    with tempfile.TemporaryDirectory() as temp_dir:
        html_files = [f for f in os.listdir(HTML_DIR) if f.endswith('.html')]
        if file_limit:
            html_files = html_files[:file_limit]
        
        total_files = len(html_files)

        # Preprocess HTML files
        preprocessed_files = []
        for index, html_file in enumerate(html_files, start=1):
            with open(os.path.join(HTML_DIR, html_file), 'r', encoding='utf-8') as f:
                content = f.read()
            
            preprocessed_content = preprocess_html(content)
            
            preprocessed_file = os.path.join(temp_dir, f'preprocessed_{html_file}')
            with open(preprocessed_file, 'w', encoding='utf-8') as f:
                f.write(preprocessed_content)
            
            preprocessed_files.append(preprocessed_file)
            print(f"Preprocessed {index}/{total_files}: {html_file}")

        print("\nGenerating PDF...")
        
        output_pdf = os.path.join(temp_dir, 'output.pdf')
        
        cmd = [PATH_TO_WKHTMLTOPDF, '--enable-local-file-access']
        
        if os.path.exists('cover.html'):
            cmd.extend(['cover', 'cover.html'])
        
        cmd.extend(preprocessed_files)
        cmd.append(output_pdf)
        
        try:
            subprocess.run(cmd, check=True)
            print("PDF generated successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error generating PDF: {str(e)}")
            return

        with open(output_pdf, 'rb') as f_in:
            with open(OUTPUT_PDF, 'wb') as f_out:
                f_out.write(f_in.read())

    print(f"\nPDF conversion complete. Output file: {OUTPUT_PDF}")