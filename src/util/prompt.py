def get_system_prompt() -> str:
   system_prompt = f"""
    
    You are the best professional career assistant. You can look at a job description and figure out exactly 
    the ideal resume and cover letter that would align with this role perfectly. You have the ability to skim through
    resumes and cover letter and give an exact score on how well this candidacy aligns with the job description. You
    have a deep understanding of what works in the resume and what can be improved with slight tweaks.
    
    You can also understand the kinds of projects that a company with such a job description could be impressed by,
    and having vast technical knowledge you can identify and come up with such projects.
    
    Your responses will always be in JSON format.
    """

   return system_prompt


def get_user_prompt(job_description, base_resume, base_cover_letter) -> str:
   user_prompt = f"""
   
   I am providing you with three inputs, a job description, my base resume, my base cover letter:
   
   Job Desciption (Text):
   {job_description}
   
   Base Resume (JSON Stringified):
   {base_resume}
   
   Base Cover Letter (Text):
   {base_cover_letter}
   
   (Note: The job description is text that is scraped from the company's website, it might contain many irrelevant words and characters, you are to assume only the relevant bit)
   
   You are tasked with the following: 
    
    1. [RESUME] My resume will be a JSON string, it will have 3 main sections, which are:
        skills, experience and projects (all of which will have their own collection of key-value pairs)
        
        You are to go through all of this as well as what you think this company looks for in this particular job description (you are to use your training data for information about this
        company, and you get the company name from the job description)
        
        Based on all of this information, you are to return the resume response in JSON with the following keys:
        
        a) resume_score: This is a score that you will assign to my base resume out of 100. The value will be of data type float (0 - 100). You need to be very critical in giving this score.
        
        b) resume_hits: This is a list of strings where you will highlight what parts of my resume are actually relevant and aligning with this job description, this information will help
                        me understand what is working so I can double down on those aspects, it may include any of the skills I have mentioned, any relevant work experience, any projects.
                        
        c) resume_fails: This is a list of string where you will highlight what parts of my resume are not relevant, and what I could improve upon. Identify the weak parts, suggest
                        changes and improvements.
                        
        d) resume_projects: This is a list of Projects that according to you are extremely relevant to this job description and this company, I will use this information to gather ideas on
                            possible projects I should work on, if I want to work at this company. The Project object itself should have a title, list of technologies used and list of highlights
                            (The format for this is included as part of the prompt forcing a Structure JSON response)
        
        Remember that for all this information you need to consider not only my resume/cover letter and job description. BUT ALSO consider what this particular company looks for in employees
        based on your training data, even if that information is not in my original context provided.
       
    You need to return the resume in JSON format
    
    2. [COVER LETTER DRAFT] Given my base cover letter I want you to generate a cover letter that best fits this job description. You should keep the general structure same but change
       some sentences and phrasing to make it more attractive to the recruiters. You know exactly what an ideal cover letter for this job looks like. You have the freedom to add
       some content that you think would elevate my candidacy. The response should be in normal text.
       
    3. [RECRUITER EMAIL DRAFT] You also need to draft an email to a recruiter of this company telling them that you are interested in this job role. Include some parts of my cover letter
       in this email. The aim of the email is to help the other person understand why my profile is such a good fit for this exact role. This needs to be short and crisp. Not more
       than 10 lines. For the name of the recruiter you should use a placeholder like [RECRUITER_NAME]. The response should be normal text.
       
    4. [RECRUITER LINKEDIN DRAFT] You also need to draft a message that can be sent to a recruiter on LinkedIn regarding this job opening. Give a crisp initial message draft that is under 200 characters.
        Highlight why my profile fits perfectly for this job. As I said, stick to 200 characters.
    
      
   Finally you also need to identify the company name from the job description and return that as part of the response as well. Your final response should be in the JSON format with
   specific keys. For resume - use key "resume" (value will be the entire resume JSON). For cover letter - use key "cover_letter_draft" (value will be the cover letter in plain text,
   but include line breaks as part of text so I can render it easily). For Recruiter Email - use key "recruiter_email_draft" (value will be plain text). For Recruiter linkedin draft - 
   use key "recruiter_linkedin_draft" (value will be plain text, limit to 200 characters). For company name - use key "company_name" (value will be plain text)
   
   """
   
   
   return user_prompt