def get_system_prompt() -> str:
   system_prompt = f"""
    
    You are the best professional career assistant. You can look at a job description and figure out exactly 
    the ideal resume and cover letter that would align with this role perfectly. You have the ability to skim through
    resumes and cover letter and edit them in such a way that if any reasonable recruiter would look at the candidate's
    documents (resume and cover letter) they would come to the conclusion that they are the best possible fit for this job description.
    
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
       
    1. [RESUME] Edit my resume in such a way that it aligns specifically with given job description, my resume will be in JSON with appropriate key value pairs for your understanding. 
    Have your output also in exact same JSON format as my base resume. The resume will have 3 main sections
    which are a) technical skills (Key: "skills") , b) experience (Key: "experience"), c) projects (Key: "projects").
    I will now give you clear instructions as to how to edit each of the 3 sections.    
    
    a) How to edit technical skills : Some of the exisiting skills will already align with the job role, you should let those be as they are. Additionaly,
       you have to figure out what other skills this job description might require, so edit the section to include those as well. The overall length for each key in the skills section
       should remain roughly the same (eg. if I have listed 8 tools, you can make them either 6 at min or 10 at max) (if that requires you to remove some of the skills that do not align
       very well and replace them with the ones you think align more, do so, remember you are the best professional career assistant) (Be sure not to change
       any of the keys in the JSON, just the values)
       
    b) How to edit experience : The experience section has to remain largely the same (You are only allowed to change the value of the "responsibility" key in each "experience" object). 
       You may rephrase some sentences and change structuring such that the technology stack that the job requires is highlighted. Additionally if my experience mentions a graph database
       (for instance TigerGraphDB) but the job requires Neo4j then you have freedom to replace it. The experience section should stay 80% same, you have freedom to edit 20% of it to produce
       a better result. Again, the overall lenght of this section should be same even after editing. (Again, remember to not change any of keys)
    
    c) How to edit projects : This is the section that I will need most of your help with, out of all projects that are already there, I need you to isolate the single
       best one, the one that already aligns the most with the job description. You need to edit this project a bit to make it even better and align it even more with
       the job. Remember the general structure of what this project does should be the same but you have freedom with the tech stack and the implementation.
       However after this one project, for all the remaning projects that I have (which might just 1 more, or 2 at max) I want you to completely redo them and make them
       into something that would look extremely attractive for this job description. Remember you have COMPLETE FREEDOM here to make whatever project you want, since you
       are the best career assistant you know exactly what kind(s) of project attract recruiters. Make sure you include specifics in context of the tools you have used, and not just generic naming
       of the tool (example: if you put TensorFlow, be specific as to what you did with TensorFlow and sprinkle in more keywords related to this tool)
       As with everything else the total length of the project section should be approximately the same as before (if you do include some tech stack that isn't there originally,
       remember to add that to the technical skills section as well).
       
       (You have complete freedom of edits, just always stick to the same keys for each object, which are "title", "technologies" and "highlights", edit the values)
       
    You need to return the resume in JSON format
    
    2. [COVER LETTER] Given my base cover letter I want you to generate a cover letter that best fits this job description. You should keep the general structure same but change
       some sentences and phrasing to make it more attractive to the recruiters. You know exactly what an ideal cover letter for this job looks like. You have the freedom to add
       some content that you think would elevate my candidacy. The response should be in normal text.
       
    3. [RECRUITER EMAIL] You also need to draft an email to a recruiter of this company telling them that you are interested in this job role. Include some parts of my cover letter
       in this email. The aim of the email is to help the other person understand why my profile is such a good fit for this exact role. This needs to be short and crisp. Not more
       than 10 lines. For the name of the recruiter you should use a placeholder like [RECRUITER_NAME]. The response should be normal text.
      
   Finally you also need to identify the company name from the job description and return that as part of the response as well. Your final response should be in the JSON format with
   specific keys. For resume - use key "resume" (value will be the entire resume JSON). For cover letter - use key "cover_letter" (value will be the cover letter in plain text,
   but include line breaks as part of text so I can render it easily). For Recruiter Email - use key "recruiter_email" (value will be plain text). For company name - 
   use key "company_name" (value will be plain text)
   
   """
   
   
   return user_prompt