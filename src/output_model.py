from pydantic import BaseModel
from typing import List, Optional

"""
This matches the exact format for the resume.json. For any changes in the original
format, update the fields here to reflect the same.
"""

class Contact(BaseModel):
    location: str
    phone: str
    email: str
    link1: Optional[str] = None
    link2: Optional[str] = None
    

class Education(BaseModel):
    institution: str
    location: str
    degree: str
    timeline: str
    

class Skills(BaseModel):
    languages: str
    frameworks: str
    tools: str
    cloud: str
    databases:str
    certifications: str
    achievements: str
    
    
class Experience(BaseModel):
    company: str
    location: str
    position: str
    timeline: str
    responsibilities: List[str]


class Project(BaseModel):
    title: str
    technologies: List[str]
    highlights: List[str]


class Resume(BaseModel):
    name: str
    contact: Contact
    education: List[Education]
    skills: Skills
    experience: List[Experience]
    projects: List[Project]
    
    
class Output(BaseModel):
    resume: Resume
    cover_letter: str
    recruiter_email: str
    company_name: str