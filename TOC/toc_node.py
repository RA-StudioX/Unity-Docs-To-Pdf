class TOCNode:
    def __init__(self, title, link):
        self.title = title
        self.link = link
        self.children = []
        self.html_content = None
        self.pdf_file = None

    def add_child(self, child):
        self.children.append(child)
    
    def add_html_content(self, html_content):
        self.html_content = html_content

    def add_pdf_file(self, pdf_file):
        self.pdf_file = pdf_file

    def get_toc_list_from_root(self):
        return self.children
    
    def __str__(self):
        return f"{self.title} ({self.link})"