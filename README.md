<p align="center">
    <a href="https://ra-studio.net" target="_blank">
        <img src="Images/RAStudio-logo.svg" alt="RA Studio Logo" width="200"/>
    </a>
</p>

# Unity Documentation PDF Converter

This project provides a command-line tool to convert Unity Documentation from HTML to PDF format. It allows users to convert specific topics or the entire documentation, with options to control the depth of conversion and specify the output file.

## Features

- Convert specific Unity Documentation topics to PDF
- Convert all Unity Documentation topics to a single PDF
- Limit the depth of conversion for hierarchical topics
- List all available topics for conversion
- Customizable output file name

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher
- pdfkit
- PyPDF2
- BeautifulSoup4
- wkhtmltopdf (installed and accessible in your system PATH)

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/RA-StudioX/Unity-Docs-To-Pdf.git
   cd unity-docs-pdf-converter
   ```

2. Install the required Python packages:

   ```
   pip install -r requirements.txt
   ```

3. Install wkhtmltopdf:

   - For Windows: Download and install from [wkhtmltopdf official site](https://wkhtmltopdf.org/downloads.html)
   - For macOS: `brew install wkhtmltopdf`
   - For Linux: `sudo apt-get install wkhtmltopdf` (Ubuntu/Debian) or `sudo yum install wkhtmltopdf` (CentOS/Fedora)

4. Update the `config.py` file with your specific paths and settings.

## Usage

The main script is `main.py`. Here are some example usages:

1. More Details

   ```
   python main.py -h
   ```

1. List all available topics:

   ```
   python main.py --list-topics
   ```

1. Convert a specific topic to PDF:

   ```
   python main.py --topic-index 0 --depth 2 --output unity_basics.pdf
   ```

1. Convert all topics to a single PDF:
   ```
   python main.py --output full_unity_docs.pdf
   ```

### Command-line Arguments

- `--topic-index`: Index of the topic to convert. If not provided, all topics will be converted.
- `--depth`: Limit the depth of the topic hierarchy to process. If not specified, all levels will be processed.
- `--output`: Output PDF file name. Default is 'output.pdf'.
- `--list-topics`: List all available topics and their indices, then exit.

## Project Structure

- `main.py`: The main script to run the conversion process.
- `cli_parser.py`: Handles command-line argument parsing and validation.
- `pdf_converter.py`: Contains the core logic for converting HTML to PDF.
- `topic_utils.py`: Utility functions for handling topics.
- `html_preprocessor.py`: Preprocesses HTML content before conversion.
- `config.py`: Configuration settings for the project.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

## License

This package is licensed under the MIT License. See the [LICENSE](https://github.com/RA-StudioX/Unity-Docs-To-Pdf/blob/main/LICENSE.md) file for details.

## Author

Rafael Azriaiev

- Email: contact@ra-studio.net
- Website: https://ra-studio.net
- GitHub: https://github.com/RA-StudioX

## Support

If you encounter any issues or have questions, please file an issue on the [GitHub repository](https://github.com/RA-StudioX/Unity-Docs-To-Pdf/issues).
