import os
import sys
import json
from handlers.pdf_handler import process_response
import util.parser as parser

from pydantic import ValidationError
from handlers.openai_handler import generate_response

# Create output directory
OUTPUT_DIR = "../output/parsed_content"
os.makedirs(OUTPUT_DIR, exist_ok=True)

URL_FILE = "../input/urls.txt"
RESUME_FILE = "../input/resume.json"
COVER_LETTER_FILE = "../input/cover_letter.txt"

# JD input per URL, set low for cost savings
MAX_CHARS = 8000

def process_urls():
    """
    Process URL from inputs
    """
    if not os.path.exists(URL_FILE):
        print(f'Err: {URL_FILE} not found')
        sys.exit(1)

    with open(URL_FILE, 'r') as f:
        url = f.readline().strip()

    if not url:
        print(f"Error: No URL found in {URL_FILE}")
        sys.exit(1)

    rendered_html = parser.fetch_page_html(url)
    if not rendered_html:
        print("Error: Could not retrieve HTML")
        sys.exit(1)

    job_description = parser.extract_job_description(rendered_html,max_chars=MAX_CHARS)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "job_description.txt")
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write(job_description)

    print(f'Saved parsed Job Description to {output_file}')
    
    base_resume = RESUME_FILE
    
    if not os.path.exists(base_resume):
        print("Error: Base resume missing.")
        sys.exit(1)
    
    try:
        with open(base_resume, 'r', encoding='utf-8') as f:
            resume_data = json.load(f)
        
        base_resume = resume_data
    
    except ValidationError as e:
        print(f'Invalid Resume JSON format: {e}')
        sys.exit(1)
    
    base_cover_letter = COVER_LETTER_FILE
    
    if not os.path.exists(base_cover_letter):
        print("Error: Base cover letter file missing.")
        sys.exit(1)
        
    with open(base_cover_letter, 'r', encoding='utf-8') as f:
        base_cover_letter = f.read()
    
    response = generate_response(job_description, base_resume, base_cover_letter)
    process_response(response)


if __name__ == "__main__":
    process_urls()