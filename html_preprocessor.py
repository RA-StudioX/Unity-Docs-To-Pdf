from bs4 import BeautifulSoup
import os

def preprocess_html(html_content, base_path):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Update relative URLs to absolute paths
    for tag in soup.find_all(['img', 'script', 'link']):
        if tag.has_attr('src'):
            src = tag['src']
            if not src.startswith(('http://', 'https://', '/')):
                tag['src'] = os.path.join(base_path, src)
        elif tag.has_attr('href'):
            href = tag['href']
            if not href.startswith(('http://', 'https://', '/')):
                tag['href'] = os.path.join(base_path, href)
    
    # Remove unwanted elements (if necessary)
    elements_to_remove = [
        '.ad-container',
        '#top-banner', 
        '.header-wrapper',
    ]
    
    for element in elements_to_remove:
        for tag in soup.select(element):
            tag.decompose()
    
    # Ensure proper encoding declaration
    if not soup.find('meta', charset=True):
        charset_tag = soup.new_tag('meta')
        charset_tag['charset'] = 'UTF-8'
        soup.head.insert(0, charset_tag)
    
    return str(soup)