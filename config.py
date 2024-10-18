import os

# Set the path to the wkhtmltopdf executable
PATH_TO_WKHTMLTOPDF = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

# Define base directories
BASE_DIR = r'd:\UnityDocumentation\Documentation\en'
HTML_DIR = os.path.join(BASE_DIR, 'Manual')
TOC_DIR = os.path.join(HTML_DIR, r'docdata\toc.json')

# Define options to include images and CSS
PDF_OPTIONS = {
    'enable-local-file-access': '',
    'encoding': "UTF-8",
    'custom-header': [
        ('Accept-Encoding', 'gzip')
    ],
    'no-outline': None,
}

# Define Table of Contents options
TOC_OPTIONS = {
    'xsl-style-sheet': 'toc.xsl'
}