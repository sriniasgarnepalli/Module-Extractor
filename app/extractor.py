from bs4 import BeautifulSoup

def extract_clean_content(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Remove irrelevant tags
    for tag in soup(['nav', 'header', 'footer', 'script', 'style', 'aside']):
        tag.decompose()

    sections = {}
    current_module = None
    current_sub = None

    for tag in soup.find_all(['h1', 'h2', 'h3', 'p', 'ul', 'ol']):
        if tag.name == 'h1':
            current_module = tag.get_text(strip=True)
            sections[current_module] = []
            current_sub = None

        elif tag.name == 'h2' and current_module:
            current_sub = {'title': tag.get_text(strip=True), 'content': []}
            sections[current_module].append(current_sub)

        elif tag.name == 'h3' and current_module:
            # Nesting under last submodule if exists, otherwise new submodule
            h3_title = tag.get_text(strip=True)
            if current_sub:
                current_sub['content'].append(f"### {h3_title}")
            else:
                sections[current_module].append({'title': h3_title, 'content': []})
                current_sub = sections[current_module][-1]

        elif tag.name in ['p', 'ul', 'ol'] and current_module and sections[current_module]:
            text = ""
            if tag.name in ['ul', 'ol']:
                items = [li.get_text(" ", strip=True) for li in tag.find_all('li')]
                text = "\n".join(f"- {item}" for item in items)
            else:
                text = tag.get_text(" ", strip=True)

            if current_sub:
                current_sub['content'].append(text)
            else:
                # If no h2 yet, create a fallback submodule
                fallback = {'title': 'General', 'content': [text]}
                sections[current_module].append(fallback)
                current_sub = fallback

    return sections
