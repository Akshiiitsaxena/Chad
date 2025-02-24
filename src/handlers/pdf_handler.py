import json
import os
import textwrap

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def save_to_pdf(content: str, file_path: str):
    c = canvas.Canvas(file_path, pagesize=letter)
    c.setFont("Helvetica", 11)

    max_width = 90  # max characters per line
    y_position = 750
    lines = content.split("\n")

    for line in lines:
        wrapped_lines = textwrap.wrap(line, width=max_width)
        if not wrapped_lines:
            # Even if line is empty, move down
            wrapped_lines = [""]

        for subline in wrapped_lines:
            c.drawString(50, y_position, subline)
            y_position -= 20

            # If we approach the bottom, create a new page
            if y_position < 50:
                c.showPage()
                c.setFont("Helvetica", 11)
                y_position = 750

    c.save()

def process_response(response_str: str, output_base_dir: str = "../output"):
    """
    Parses the OpenAI response JSON, extracts cover letter and recruiter drafts,
    and saves them as PDFs in a company-specific folder.
    """
    try:
        data = json.loads(response_str)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return

    company_name_raw = data.get("company_name", "Generic").strip()
    cover_letter = data.get("cover_letter_draft", "").strip()
    recruiter_email = data.get("recruiter_email_draft", "").strip()
    recruiter_linkedin = data.get("recruiter_linkedin_draft", "").strip()
    
    resume_review = data.get("resume", {})

    # Sanitize company name for folder name
    company_name = company_name_raw.replace(" ", "_")
    
    company_folder = os.path.join(output_base_dir, company_name)
    os.makedirs(company_folder, exist_ok=True)

    # Build PDF file paths
    cover_letter_filename = f"{company_name}_cover_letter.pdf" if company_name_raw else "cover_letter.pdf"
    recruiter_email_filename = f"{company_name}_email.pdf" if company_name_raw else "email.pdf"
    recruiter_linkedin_filename = f"{company_name}_linkedin.pdf" if company_name_raw else "linkedin.pdf"

    cover_letter_path = os.path.join(company_folder, cover_letter_filename)
    recruiter_email_path = os.path.join(company_folder, recruiter_email_filename)
    recruiter_linkedin_path = os.path.join(company_folder, recruiter_linkedin_filename)

    if cover_letter:
        save_to_pdf(cover_letter, cover_letter_path)
        print(f"Saved Cover Letter PDF: {cover_letter_path}")

    if recruiter_email:
        save_to_pdf(recruiter_email, recruiter_email_path)
        print(f"Saved Recruiter Email PDF: {recruiter_email_path}")

    if recruiter_linkedin:
        save_to_pdf(recruiter_linkedin, recruiter_linkedin_path)
        print(f"Saved Recruiter LinkedIn PDF: {recruiter_linkedin_path}")
    
    review_file_name = f"{company_name}_resume_review.json" if company_name_raw else "resume_review.json"
    review_file_path = os.path.join(company_folder, review_file_name)

    with open(review_file_path, "w", encoding="utf-8") as f:
        json.dump(resume_review, f, indent=2)
    print(f"Saved resume review JSON: {review_file_path}")