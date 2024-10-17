from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
from reportlab.platypus.doctemplate import BaseDocTemplate, PageTemplate, Frame
from reportlab.platypus.frames import Frame

class MyDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kw):
        self.allowSplitting = 0
        BaseDocTemplate.__init__(self, filename, **kw)
        template = PageTemplate('normal', [Frame(inch, inch, 6.5*inch, 9*inch, id='F1')])
        self.addPageTemplates(template)

    def afterFlowable(self, flowable):
        "Registers TOC entries."
        if flowable.__class__.__name__ == 'Paragraph':
            text = flowable.getPlainText()
            style = flowable.style.name
            if style == 'Heading1':
                key = 'h1-%s' % self.seq.nextf('heading1')
                self.canv.bookmarkPage(key)
                self.notify('TOCEntry', (0, text, self.page, key))
            if style == 'Heading2':
                key = 'h2-%s' % self.seq.nextf('heading2')
                self.canv.bookmarkPage(key)
                self.notify('TOCEntry', (1, text, self.page, key))

def create_pdf_with_toc(filename):
    doc = MyDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Register a custom font (optional)
    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    
    # Modify existing styles
    styles['Heading1'].fontName = 'Vera'
    styles['Heading1'].fontSize = 16
    styles['Heading1'].leading = 20

    styles['Heading2'].fontName = 'Vera'
    styles['Heading2'].fontSize = 14
    styles['Heading2'].leading = 18
    styles['Heading2'].leftIndent = 10

    styles['BodyText'].fontName = 'Vera'
    styles['BodyText'].fontSize = 12
    styles['BodyText'].leading = 14
    
    # Create and add Table of Contents
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle(fontName='Vera', fontSize=14, name='TOCHeading1', leftIndent=20, firstLineIndent=-20),
        ParagraphStyle(fontName='Vera', fontSize=12, name='TOCHeading2', leftIndent=40, firstLineIndent=-20),
    ]
    story.append(Paragraph('Table of Contents', styles['Heading1']))
    story.append(toc)
    story.append(PageBreak())
    
    # Add content
    for i in range(1, 4):
        story.append(Paragraph(f'Chapter {i}', styles['Heading1']))
        story.append(Spacer(1, 0.2 * inch))
        story.append(Paragraph('This is the introduction to the chapter. ' * 3, styles['BodyText']))
        story.append(PageBreak())
        
        for j in range(1, 4):
            story.append(Paragraph(f'Section {i}.{j}', styles['Heading2']))
            story.append(Spacer(1, 0.2 * inch))
            story.append(Paragraph('Lorem ipsum dolor sit amet, consectetur adipiscing elit. '
                                   'Donec a diam lectus. Sed sit amet ipsum mauris. ' * 3, styles['BodyText']))
            story.append(PageBreak())
    
    # Build the PDF
    doc.multiBuild(story)

# Create the PDF
create_pdf_with_toc('example_with_toc.pdf')