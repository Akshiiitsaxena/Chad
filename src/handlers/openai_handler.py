from openai import OpenAI
import json
import os

import util.prompt as prompt
from model.output_model import Output

# Load API key from config 
CONFIG_FILE = "../config/config.json"

def load_api_key():
    """
    Load OpenAI API key from the config file
    """
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Config file not found: {CONFIG_FILE}")
    
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
        return config.get("apiKey")

def generate_response(job_description, base_resume, base_cover_letter):
    """
    Send job description, base resume, and base cover letter
    """
    openai_api_key = load_api_key()
    if not openai_api_key:
        raise ValueError("OpenAI API key not found in config.json.")

    client = OpenAI(api_key=openai_api_key)

    system_prompt = prompt.get_system_prompt()
    user_prompt = prompt.get_user_prompt(job_description, base_resume, base_cover_letter)
    
    try:
        response = client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": user_prompt}],
            max_tokens=10000,
            temperature=0.8,  # Creativity level
            store=True,
            response_format=Output
        )
        
        response_json = response.choices[0].message.content
        
        return response_json

    except Exception as e:
        print(f"Error generating response from OpenAI: {e}")
        return None