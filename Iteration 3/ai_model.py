# This file is where I interface with the Google Gemini AI LLM 
# to generate a workout routine based on information provided by the user.

import json
from sys import exit
from time import sleep
from google import genai
from pygame import quit

from utils import app_manager
from ui_elements import workout_generation_form_elements, home_elements, loading_elements

# Try to get setup the AI client, if an exception occurs, tell the user how to set up the ai
try:
    # Store the API key in a .env file for security purposes, DONT PUSH THE .ENV FILE TO GITHUB
    # Instructions for what to do are in the README.md file
    client = genai.Client()
except:
    print("\n!!! Please check the README.md file for instructions to get the AI model working !!!\n")
    print("\n!!! Please check the README.md file for instructions to get the AI model working !!!\n")
    quit() # Quit pygame, closes the window
    sleep(15) # Wait 15 seconds so that the user has plenty of time to read the console output
    exit() # Close the python program

def generate_workout(data: dict): 
    # Set the loading state
    app_manager.change_state("Loading", loading_elements, workout_generation_form_elements)
    
    # Hide and disable the navigation icons
    
    
    # Create custom prompt based on user data
    prompt = f'''
        Generate an at-home workout for this user who has provided this information about themselves:
        age: {data["age"]}
        injuries: {data["injuries"]}
        physical disabilities: {data["disabilities"]}
        time available per day in minutes: {data["availability"]}
        weight (assume kilograms if not specified): {data["weight"]}
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
        Important:
            - The output **must be valid JSON parsable by Python's `json` module**.
            - Do not include comments or text outside the JSON.
            - Adapt or exclude any exercises which may aggrivate the user's injuries or physical disabilities (if they have any).
    '''
    
    # send prompt to the AI LLM and wait for a response
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
    )
    
    # Remove unwanted backticks from the LLM output
    cleaned_response = response.text.replace("```json", "").replace("```", "").strip()
    print(cleaned_response)
    
    # Convert string to a json-like object (list in this case) and save it
    app_manager.workout = json.loads(cleaned_response)
    app_manager.save_workout()
    
    # Change to home state
    app_manager.change_state("Home", home_elements, loading_elements)
