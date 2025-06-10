# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
#
#
# def crawl(url, visited=None, depth=2):
#     if visited is None:
#         visited = set()
#     if url in visited or depth == 0:
#         return []
#
#     visited.add(url)
#     try:
#         res = requests.get(url, timeout=5)
#         res.raise_for_status()
#         soup = BeautifulSoup(res.text, 'html.parser')
#         links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]
#         filtered_links = [link for link in links if url in link]
#     except Exception:
#         return []
#
#     all_links = [url]
#     for link in filtered_links:
#         all_links.extend(crawl(link, visited, depth - 1))
#
#     return list(set(all_links))


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse

def normalize_url(url):
    parsed = urlparse(url)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))

def is_valid_link(base_url, link):
    if not link.startswith(base_url):
        return False
    skip_exts = (".jpg", ".png", ".pdf", ".css", ".js", ".svg", ".ico")
    return not any(link.lower().endswith(ext) for ext in skip_exts)

def crawl(url, visited=None, depth=2, max_pages=50):
    if visited is None:
        visited = set()

    url = normalize_url(url)
    if url in visited or depth == 0 or len(visited) >= max_pages:
        return []

    visited.add(url)
    try:
        res = requests.get(url, timeout=8)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        all_links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]
        filtered_links = [normalize_url(link) for link in all_links if is_valid_link(url, link)]
    except Exception:
        return []

    result_links = [url]
    for link in filtered_links:
        if len(visited) >= max_pages:
            break
        result_links.extend(crawl(link, visited, depth - 1, max_pages))

    return list(set(result_links))
