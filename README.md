# Chad 💯

Applying to jobs is boring and repetitive at best, and downright draining at worst. Everyone’s approach is different, but most people try to optimize for two things:

1. **Number of applications** filled.
2. **Quality of each application**.

It doesn’t take a genius to see that if you have a cap on time, these two factors are **inversely proportional**: the more time you spend on each application, the fewer applications you can submit.

So this is where Chad comes in!

**Chad** is an open-source Python program that helps you manage this trade-off. By providing your resume, cover letter, and a job posting URL, Chad will:

1. Give you a **Resume Score** (out of 100).
2. List **Resume Hits**: what works in your resume.
3. List **Resume Fails**: what doesn’t work in your resume. And how to improve it.
4. List **Resume Projects**: Some Project ideas that it thinks can be attractive for such a job.
5. Generate a **Cover Letter Draft** specific to the job description, saved as a PDF.
6. Generate an **Email Draft** you can send to a recruiter.
7. Generate a **Short LinkedIn Message** for reaching out to recruiters (keeping in mind the 200 Character limit for non-premium users)

---

## Requirements

- **Python 3.8+**
- [**pip**](https://pip.pypa.io/en/stable/) for installing dependencies
- The following Python libraries:
- `requests`
- `beautifulsoup4`
- `playwright`
- `openai`
- `pydantic`
- `reportlab`
- You’ll also need:
- An **OpenAI API key** in your `config/config.json` file.
- A folder structure similar to:

```
Chad/
├── config/
│ └── config.json           # Contains your OPENAI_API_KEY
├── input/
│ ├── resume.json           # Your JSON-formatted resume
│ └── cover_letter.txt      # Your base cover letter (plain text)
├── output/
│ └── ...                   # Generated PDFs and review JSONs go here
└── src/
  └── ...                   # Python scripts for Chad
```

---

## Setup

1. **Clone the Repository:**

```bash
git clone https://github.com/Akshiiitsaxena/Chad.git
cd Chad
```

2. **Create a Virtual Environment (Recommended):**

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

3. **Install Dependencies:**

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install requests beautifulsoup4 playwright openai pydantic reportlab
playwright install chromium
```

4. **Add Your OpenAI API Key:**
   Create a file `config/config.json`:

```json
{
  "openai_api_key": "sk-1234..."
}
```

5. **Prepare Your Resume & Cover Letter:**

- **`resume.json`**: Convert your resume into a JSON structure.
- **`cover_letter.txt`**: Plain text file with your general cover letter.

---

## Usage

1. **Parse the Job Description**
   Chad fetches the job posting’s text from the URL using [Playwright](https://playwright.dev/python/)

- Make sure the URL is placed in `input/urls.txt`

2. **Run Chad**
   In your terminal:

```bash
python src/generate.py
```

- The script will:
- Parse the job posting.
- Read your `resume.json` and `cover_letter.txt`.
- Call the OpenAI API to tailor your resume/cover letter.
- Save outputs (PDFs, JSON reviews) in the `output/` folder.

3. **Outputs**

- **`companyname_cover_letter.pdf`**: Tailored cover letter PDF.
- **`companyname_email.pdf`**: Draft email to send to a recruiter.
- **`companyname_linkedin.pdf`**: Short LinkedIn message (under 200 chars).
- **`companyname_resume_review.json`**: Info about your resume’s hits, fails, and recommended project sections.

---

## Why Use Chad?

- **Save Time**: Focus on many high-quality applications, not repetitive cover letter rewriting.
- **Objective Insights**: See your resume’s strengths and weaknesses for each job.
- **Automate Customization**: AI-driven tailoring for each job posting.

---

## Contributing

Contributions are welcome! Feel free to open issues or pull requests for:

- New features or improvements.
- Bug fixes and performance enhancements.
- Additional AI-driven insights on resumes or cover letters.

---

**Happy Job Hunting with Chad!**
