class TOCNode:
    def __init__(self, title, link=None):
        self.title = title
        self.link = link
        self.children = []
        self.content = None
        self.page_number = 1  # Default page number

    def add_child(self, child_node):
        self.children.append(child_node)
    
    def add_content(self, content):
        self.content = content

    def update_page_number(self, page_number):
        self.page_number = page_number

    def get_toc(self, indent=0):
        toc = f"{'  ' * indent}• [{self.title}]({self.link or ''}) ......... {self.page_number}\n"
        for child in self.children:
            toc += child.get_toc(indent + 1)
        return toc

    def to_dict(self):
        return {
            "title": self.title,
            "link": self.link,
            "children": [child.to_dict() for child in self.children]
        }