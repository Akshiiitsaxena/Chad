from pydantic import BaseModel
from typing import List


class Project(BaseModel):
    title: str
    technologies: List[str]
    highlights: List[str]


class Resume(BaseModel):
    resume_score: float
    resume_hits: List[str]
    resume_fails: List[str]
    resume_projects: List[Project]
    
    
class Output(BaseModel):
    resume: Resume
    cover_letter_draft: str
    recruiter_email_draft: str
    recruiter_linkedin_draft: str
    company_name: str