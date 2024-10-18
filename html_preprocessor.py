from bs4 import BeautifulSoup

def preprocess_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove unwanted elements
    elements_to_remove = [
        'header',  # Example: remove header
        'nav',     # Example: remove navigation
        '.ad-container',  # Example: remove elements with class 'ad-container'
        '#top-banner'  # Example: remove element with id 'top-banner'
    ]
    
    for element in elements_to_remove:
        for tag in soup.select(element):
            tag.decompose()
    
    return str(soup)