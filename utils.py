# This file is used to initialise and define various constants and utility functions which will be used throughout the app

import pygame
import json

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


def extract_json(text: str) -> str:
    cleaned_data = text.replace("```json", "").replace("```", "").strip()
    return cleaned_data

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
        
        self.states = {
            "Onboarding": False,
            "Home": False,
        }

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
    
    def change_state(self, new_state: str, elements_to_show: list, elements_to_hide: list):
        # Make sure the new_state parameter is valid,
        # then update the states dictionary.
        if new_state in self.states:
            for state in self.states:
                self.states[state] = False
            self.states[new_state] = True

            # Show all the neccessary elements
            for element in elements_to_show:
                element.show()
                element.enable()
            
            # Hide all the neccessary elements
            for element in elements_to_hide:
                element.hide()

        # If the state_to_change_to was invalid, then print "Invalid State"
        else:
            print("Invalid State")


app_manager = AppManager()