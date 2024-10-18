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
- List all available topics and subtopics for conversion
- Navigate through the topic hierarchy
- Print full topic tree
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
   cd Unity-Docs-To-Pdf
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

1. Show help and available options:

   ```
   python main.py -h
   ```

2. List all available topics:

   ```
   python main.py --list-topics
   ```

3. Convert a specific topic to PDF:

   ```
   python main.py --topic-path 0/1/2 --depth 2 --output unity_specific_topic.pdf
   ```

4. Convert all topics to a single PDF:

   ```
   python main.py --output full_unity_docs.pdf
   ```

5. Print the full topic tree:

   ```
   python main.py --full-tree
   ```

### Command-line Arguments

- `--depth`: Limit the depth of the topic hierarchy to process. If not specified, all levels will be processed.
- `--topic-path`: Path to the topic to convert. Use slash-separated integers to specify the path to the desired topic/subtopic. Example: '0/1/2'
- `--output`: Output PDF file name. Default is 'output.pdf'.
- `--list-topics`: List topics and subtopics. Use slash-separated integers to specify the path to the desired topic/subtopic, or 'all' to list main topics.
- `--full-tree`: Print the full topic tree with all subtopics and their indices.

## Project Structure

- `main.py`: The main script to run the conversion process.
- `cli_parser.py`: Handles command-line argument parsing and validation.
- `pdf_converter.py`: Contains the core logic for converting HTML to PDF.
- `topic_utils.py`: Utility functions for handling topics and navigation.
- `html_preprocessor.py`: Preprocesses HTML content before conversion.
- `config.py`: Configuration settings for the project.
- `TOC/`: Directory containing modules for handling the table of contents
  - `__init__.py`: Initialization file for the TOC package
  - `parse_json_toc.py`: Functions for parsing the JSON table of contents
  - `toc_node.py`: Defines the TOCNode class for representing the topic hierarchy

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/RA-StudioX/Unity-Docs-To-Pdf/blob/main/LICENSE.md) file for details.

## Author

Rafael Azriaiev

- Email: contact@ra-studio.net
- Website: https://ra-studio.net
- GitHub: https://github.com/RA-StudioX

## Support

If you encounter any issues or have questions, please file an issue on the [GitHub repository](https://github.com/RA-StudioX/Unity-Docs-To-Pdf/issues).
