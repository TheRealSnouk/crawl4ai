import sys
import os
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import time
from collections import deque

def extract_content(html, url, base_domain, start_path):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Remove header, footer, and other noise
    for tag in soup(['header', 'footer', 'nav', 'script', 'style', 'aside']):
        tag.decompose()
    
    # Extract text (simple markdown-like conversion)
    text = soup.get_text(separator='\n\n', strip=True)
    
    # Get internal links
    links = set()
    
    for a in soup.find_all('a', href=True):
        href = a['href']
        full_url = urljoin(url, href)
        # Remove fragments and queries to avoid duplicates
        full_url = full_url.split('#')[0].split('?')[0].rstrip('/')
        
        parsed = urlparse(full_url)
        
        # Check if internal and stays within the starting path (to avoid crawling the whole domain)
        if parsed.netloc == base_domain and parsed.path.startswith(start_path):
            if not any(full_url.endswith(ext) for ext in ['.pdf', '.zip', '.png', '.jpg', '.jpeg', '.gif']):
                 links.add(full_url)
                 
    return text, links

def crawl_site(start_url, max_pages=100):
    print(f"Starting deep crawl for: {start_url}")
    
    parsed_start = urlparse(start_url)
    base_domain = parsed_start.netloc
    # Get the base path to ensure we stay within the relevant documentation section
    start_path = '/'.join(parsed_start.path.split('/')[:-1]) if '.' in parsed_start.path.split('/')[-1] else parsed_start.path
    if not start_path.endswith('/'):
        start_path += '/'

    results = []
    visited = set()
    queue = deque([start_url.rstrip('/')])
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    pages_crawled = 0
    
    while queue and pages_crawled < max_pages:
        url = queue.popleft()
        if url in visited:
            continue
            
        visited.add(url)
        pages_crawled += 1
        
        print(f"[{pages_crawled}/{max_pages}] Crawling: {url}")
        
        try:
            # Be polite
            time.sleep(0.5)
            
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # Ensure it's HTML
            if 'text/html' not in response.headers.get('Content-Type', ''):
                continue

            content_text, internal_links = extract_content(response.text, url, base_domain, start_path)
            
            results.append(f"# Page: {url}\n\n{content_text}\n\n")
            
            # Add new links to queue
            for link in internal_links:
                if link not in visited:
                    queue.append(link)
                    
        except Exception as e:
            print(f"Failed to crawl {url}: {e}")

    output_filename = "crawled_content_full.md"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write("\n---\n\n".join(results))
    
    print(f"\nAll done! Crawled {pages_crawled} pages. Content saved to {output_filename}")

if __name__ == "__main__":
    print("Script started")
    if len(sys.argv) > 1:
        start_url = sys.argv[1]
        # Optional: allow specifying max pages
        max_p = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    else:
        print("Usage: python crawler.py <url> [max_pages]")
        sys.exit(1)
    
    crawl_site(start_url, max_pages=max_p)
