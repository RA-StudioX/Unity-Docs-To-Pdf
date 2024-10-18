from bs4 import BeautifulSoup
import os
import re

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
    
    # Remove unwanted elements
    elements_to_remove = [
        '.ad-container',
        '#top-banner', 
        '.header-wrapper',
        '.footer-wrapper',
        '.sidebar',
        '.nextprev',
    ]
    
    for element in elements_to_remove:
        for tag in soup.select(element):
            tag.decompose()
    
    # Modify styles of specific elements
    modify_styles(soup, '.master-wrapper', {'padding': '0'})
    
    # Ensure proper encoding declaration
    if not soup.find('meta', charset=True):
        charset_tag = soup.new_tag('meta')
        charset_tag['charset'] = 'UTF-8'
        soup.head.insert(0, charset_tag)
    
    return str(soup)

def modify_styles(soup, selector, styles):
    for element in soup.select(selector):
        current_style = element.get('style', '')
        for property, value in styles.items():
            pattern = re.compile(rf'{property}\s*:\s*[^;]+;?')
            if pattern.search(current_style):
                current_style = pattern.sub(f'{property}: {value};', current_style)
            else:
                current_style += f' {property}: {value};'
        element['style'] = current_style.strip()