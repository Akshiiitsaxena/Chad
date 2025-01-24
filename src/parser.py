import os
import requests
from bs4 import BeautifulSoup
# Create output directory
OUTPUT_DIR = "../output/parsed_content"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Input file containing URLs
URL_FILE = "../input/urls.txt"

# JD input per URL, set low for cost savings
MAX_CHARS = 100000

def extract_job_description(soup: BeautifulSoup) -> str:
    """
    Extract job description text from a BeautifulSoup object.
    Balances capturing relevant sections without returning an entire noisy page.
    """
    
    known_selectors = [
         '#jobDescription',
        '.job-description',
        '.jobDescription',
        '.description',
        '.jobdesc'
        ];
    
    collected_sections = []
    
    for selector in known_selectors:
        element = soup.select_one(selector)
        if element:
            text = element.get_text(separator="\n", strip=True)
            if text:
                collected_sections.append(text)
    
    
    if collected_sections:
        return "\n\n".join(collected_sections)
    
    keywords = ['responsibilities', 'requirements', 'qualifications', 'skills', 'benefits']
    sections = soup.find_all(['div', 'section'])
    
    for section in sections:
        section_text = section.get_text(separator="\n", strip=True)
        lowercase_text = section_text.lower()
        
        if any(kw in lowercase_text for kw in keywords):
            # skip v short sections
            if len(section_text) > 50:
                collected_sections.append(section_text)
        
    if not collected_sections:
        page_text = soup.get_text(separator="\n", strip=True)
        return page_text
    
    combined_text = "\n\n".join(collected_sections)
    
    if len(combined_text) > MAX_CHARS:
        combined_text = combined_text[:MAX_CHARS] + "\n[TRUNCATED]"
        
    return combined_text
    
    
def fetch_and_parse_url(url):
    """
    Fetch a URL and parse the main content using BeautifulSoup.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses

        # Parse the content
        soup = BeautifulSoup(response.content, 'html.parser')
        job_description = extract_job_description(soup)

        return job_description
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def process_urls():
    """
    Process each URL from the input file and save the parsed content.
    """
    urls = []
    with open(URL_FILE, 'r') as file:
        lines = file.readlines()
        for line in lines:
            stripped_line = line.strip()
            if stripped_line:  # Only add non-empty lines
                urls.append(stripped_line)

    for i, url in enumerate(urls, start=1):
        print(f"Processing {i}/{len(urls)}: {url}")
        content = fetch_and_parse_url(url)

        if content:
            # Save the parsed content to a file
            output_file = os.path.join(OUTPUT_DIR, f"url_{i}.txt")
            with open(output_file, 'w', encoding='utf-8') as out_file:
                out_file.write(content)
            print(f"Saved content to {output_file}")
        else:
            print(f"Failed to process {url}")


if __name__ == "__main__":
    process_urls()