from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def create_toc_pdf(toc_nodes, output_file):
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Create a custom style for the main title
    styles.add(ParagraphStyle(name='MainTitle',
                              fontName='Helvetica-Bold',
                              fontSize=24,
                              alignment=1,  # Center alignment
                              spaceAfter=0.5*inch))

    # Function to get TOC style, creating it if it doesn't exist
    def get_toc_style(level):
        style_name = f'TOC{level}'
        if style_name not in styles:
            styles.add(ParagraphStyle(name=style_name,
                                      fontSize=max(16 - level*2, 8),  # Minimum font size of 8
                                      leftIndent=20*level))
        return styles[style_name]

    def create_toc_content(nodes, story, level=1):
        for node in nodes:
            # Add the entry to the story
            story.append(Paragraph(node.title, get_toc_style(level)))
            # Add the entry to the TOC
            toc.addEntry(level, node.title, story.__len__())
            
            if node.children:
                create_toc_content(node.children, story, level+1)

    # Create the content
    story = [
        Paragraph("Unity Documentation", styles['MainTitle']),
        Spacer(1, 0.25 * inch),
        Paragraph("Table of Contents", styles['Title']),
        Spacer(1, 0.25 * inch)
    ]

    # Create Table of Contents object
    toc = TableOfContents()
    toc.levelStyles = [get_toc_style(i) for i in range(1, 10)]  # Support up to 9 levels
    story.append(toc)

    # Add a page break after TOC
    story.append(Spacer(1, 1*inch))

    # Create the actual content (this will be used to generate TOC)
    create_toc_content(toc_nodes, story)

    # Build the PDF
    doc.multiBuild(story)