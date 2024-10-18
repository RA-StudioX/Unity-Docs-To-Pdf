import argparse
from pdf_converter import convert_pdfs

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert HTML files to PDF with optional file limit.")
    parser.add_argument("--limit", type=int, help="Limit the number of files to process")
    args = parser.parse_args()

    convert_pdfs(args.limit)