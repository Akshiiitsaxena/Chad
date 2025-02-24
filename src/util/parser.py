from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time

from pydantic import ValidationError
from handlers.openai_handler import generate_response
from model.output_model import Resume


def find_fuzzy_selectors(soup, keywords):
    """
    Search for elements where class or ID matches any of the given keywords.
    """
    collected_sections = []
    for element in soup.find_all(True):
        # Check class names
        if element.has_attr("class"):
            class_list = " ".join(element["class"]).lower()
            if any(keyword in class_list for keyword in keywords):
                text = element.get_text(separator="\n", strip=True)
                if text:
                    collected_sections.append(text)

        # Check ID names
        if element.has_attr("id"):
            element_id = element["id"].lower()
            if any(keyword in element_id for keyword in keywords):
                text = element.get_text(separator="\n", strip=True)
                if text:
                    collected_sections.append(text)

    return collected_sections

def extract_semantic_sections(soup):
    """
    Look for headings (h1-h3) or similar tags with job-related keywords
    and extract their nearby content.
    """
    keywords = ["job description", "responsibilities", "qualifications", "role"]
    collected_sections = []

    for heading in soup.find_all(["h1", "h2", "h3", "strong", "b"]):  # Heading tags or bold text
        heading_text = heading.get_text(strip=True).lower()
        if any(keyword in heading_text for keyword in keywords):
            # Grab the parent or next sibling content
            parent = heading.find_parent() or heading.find_next_sibling()
            if parent:
                text = parent.get_text(separator="\n", strip=True)
                collected_sections.append(text)

    return collected_sections

def extract_job_description(html, max_chars=8000):
    """
    Extract job description text from a BeautifulSoup object.
    Balances capturing relevant sections without returning an entire noisy page.
    """
    soup = BeautifulSoup(html, 'html.parser')

    # Fuzzy matching for class/ID names
    fuzzy_keywords = ["job", "description", "details", "summary", "posting"]
    collected_sections = find_fuzzy_selectors(soup, fuzzy_keywords)

    # Exact selectors if fuzzy matching does not yield results
    if not collected_sections:
        known_selectors = [
            '#jobDescription', '.job-description', '.jobDescription',
            '.description', '.jobdesc', ".job-details__section", ".job__description"
        ]

        for selector in known_selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(separator="\n", strip=True)
                if text:
                    collected_sections.append(text)

    # Semantic heading-based extraction
    if not collected_sections:
        collected_sections = extract_semantic_sections(soup)

    # Fallback to keyword-based section parsing
    if not collected_sections:
        keywords = ["responsibilities", "requirements", "qualifications", "skills", "benefits"]
        sections = soup.find_all(['div', 'section'])
        for section in sections:
            section_text = section.get_text(separator="\n", strip=True)
            lowercase_text = section_text.lower()
            if any(kw in lowercase_text for kw in keywords):
                collected_sections.append(section_text)

    # Fallback to entire page text (avoid if possible, huge number of input tokens)
    if not collected_sections:
        page_text = soup.get_text(separator="\n", strip=True)
        return page_text

    # Combine relevant sections
    combined_text = "\n\n".join(collected_sections)
    if len(combined_text) > max_chars:
        combined_text = combined_text[:max_chars] + "\n[TRUNCATED]"

    return combined_text

def fetch_page_html(url):
    """
    Uses Playwright to open a JS-heavy page and return the rendered HTML.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="load")
            
            # wait 3 seconds to JS to load completely
            time.sleep(3)
            
            html = page.content()
            browser.close()
            return html
    except Exception as e:
        print(f'Error loading {url} with Playwright: {e}')
        return None