from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
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

    # Create a custom style for TOC entries
    styles.add(ParagraphStyle(name='TOC',
                              fontName='Helvetica',
                              fontSize=12,
                              alignment=1,  # Center alignment
                              spaceAfter=6))

    def create_toc_content(node, level=0):
        content = []
        indent = '    ' * level
        link = node.link if node.link else ''
        
        toc_entry = f"{indent}<a href='{link}'>{node.title}</a>"
        page_num = str(node.page_number)
        
        # Create a table for each entry to allow for centered text and right-aligned page number
        toc_table = Table([[toc_entry, page_num]], colWidths=[6.5*inch, 0.5*inch])
        toc_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (0,0), 'CENTER'),
            ('ALIGN', (1,0), (1,0), 'RIGHT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 12),
        ]))
        
        content.append(toc_table)
        
        for child in node.children:
            content.extend(create_toc_content(child, level + 1))
        
        return content

    # Create the content
    content = [
        Paragraph("Unity Documentation", styles['MainTitle']),
        Spacer(1, 0.25 * inch),
        Paragraph("Table of Contents", styles['Title']),
        Spacer(1, 0.25 * inch)
    ]
    
    for node in toc_nodes:
        content.extend(create_toc_content(node))

    # Build the PDF
    doc.build(content)