import json
import os
from google import genai

from utils import app_manager
from ui_elements import onboarding_elements, home_elements

# Store the API key in a .env file for security purposes, DONT PUSH THE .ENV FILE TO GITHUB
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_workout(data: dict):
    prompt = f'''
        Generate an at-home workout for this user who has provided this information about themselves:
        age: {data["age"]}
        injuries: {data["injuries"]}
        physical disabilities: {data["disabilities"]}
        time available per day in minutes: {data["availability"]}
        other information: {data["other_information"]}
    ''' + '''
        only output json.
        ensure the workout can be reasonably finished within the time available per day.
        Generate the workout as a list of exercises in json with the format:
            [
                {
                    "name": "string, name of the exercise",
                    "description": "string, description of the exercise with brief instructions",
                    "reps": "int, number of reps",
                    "sets": "int, number of sets"
                }
            ]
    '''
    
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
    )
    
    # Remove unwanted backticks from the LLM's output
    cleaned_response = response.text.replace("```json", "").replace("```", "").strip()
    print(cleaned_response)
    
    # Convert string to a json-like object (list in this case) and save it
    app_manager.workout = json.loads(cleaned_response)
    app_manager.save_workout()
    
    app_manager.change_state("Home", home_elements, onboarding_elements)
