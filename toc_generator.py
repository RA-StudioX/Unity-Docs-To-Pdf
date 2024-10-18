from PyPDF2 import PdfReader

def extract_toc(pdf_path):
    reader = PdfReader(pdf_path)
    toc = []
    
    def process_outline(outline, depth=0):
        for item in outline:
            if isinstance(item, list):
                process_outline(item, depth + 1)
            else:
                toc.append(("  " * depth) + item.title)
    
    process_outline(reader.outline)
    return toc

# Usage
pdf_path = "your_pdf_file.pdf"
table_of_contents = extract_toc(pdf_path)

for entry in table_of_contents:
    print(entry)