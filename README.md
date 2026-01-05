# Simple Web Scraper (crawl4ai)
Deep web crawler for documentation and static sites.

This project contains a Python script to crawl a web page and its internal sub-links, converting the content into LLM-readable text, while removing headers and footers.

**Note:** This scraper uses `requests` and `BeautifulSoup` instead of `crawl4ai`/`playwright` due to compatibility issues with Python 3.14 on the current environment. It works for static sites but may not handle JavaScript-heavy content.

## Prerequisites

- Python 3.8+
- `pip`

## Setup

1.  Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the crawler with a URL:

```bash
.\venv\Scripts\python crawler.py https://example.com
```

Or using the batch file (Windows):

```bash
.\run_crawler.bat https://example.com
```

The script will:
1.  Crawl the main page.
2.  Find all internal links on the main page.
3.  Recursively crawl discovered sub-links (limited to 100-500 pages to avoid overload).
4.  Remove header, footer, nav, script, and style tags.
5.  Save all content to `crawled_content_full.md`.
