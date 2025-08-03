# This file is used to initialise and define various constants and utility functions which will be used throughout the app

import pygame
import json
from google import genai
import re

import os
from dotenv import load_dotenv

from user import User

# Initialise pygame
pygame.init()

# Load environment variables
load_dotenv()

# Sets the initial screen dimensions in pixels
# "SCREEN" refers to the window, not the computer screen, this is pygame convention
SCREEN_WIDTH = 378
SCREEN_HEIGHT = 700

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Creates a window
pygame.display.set_caption("Fit4All") # Sets the title of the window


FPS = 60 # This variable defines the desired framerate/refresh rate for the rindow
clock = pygame.time.Clock() # Instantiate the pygame Clock, this is used to keep track of the framerate

# Store the API key in a .env file for security purposes, DONT PUSH THE .ENV FILE TO GITHUB
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def extract_json(text: str) -> str:
    cleaned_data = text.replace("```json", "").replace("```", "").strip()
    return cleaned_data

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
    
    # Convert string to a json-like object and save it
    app_manager.workout = json.loads(cleaned_response)
    app_manager.save_workout()
    

class SaveManager:
    def save(self, filename, data):
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    def load(self, filename):
        if os.path.exists(filename): # Check if file exists
            with open(filename, "r") as file:
                return json.load(file) # Return the data

class AppManager:
    def __init__(self):
        self.user = None
        self.workout = []
        
        self.save_manager = SaveManager()
        
        self.user_file_name = "user.json"
        self.workout_file_name = "workout.json"

    def set_user(self, age, injuries, disabilities, availability, other_information):
        self.user = User(age, injuries, disabilities, availability, other_information)

    def save_user(self):
        self.save_manager.save(self.user_file_name, self.user.data)
    
    def load_user(self):
        # Get the data from the user.json, which is a dictionary, and convert the values to a list
        user_data = self.save_manager.load(self.user_file_name)
        
        if user_data:
            cleaned_user_data = list(user_data.values())
            
            # The * is the unpack operator, 
            # it allows me to pass all the elements in the list as arguments for the user object 
            self.user = User(*cleaned_user_data)
            
    def save_workout(self):
        self.save_manager.save(self.workout_file_name, self.workout)
    
    def load_workout(self):
        workout_data = self.save_manager.load(self.workout_file_name)
        
        if workout_data:
            self.workout = workout_data

app_manager = AppManager()