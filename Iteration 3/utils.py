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

# Change the working directory of the program to the folder that this
file_path = os.path.abspath(__file__)
os.chdir(os.path.dirname(file_path))


FPS = 60 # This variable defines the desired framerate/refresh rate for the rindow
clock = pygame.time.Clock() # Instantiate the pygame Clock, this is used to keep track of the framerate

# SaveManager class
class SaveManager:
    # Save method
    def save(self, filename, data):
        with open(filename, "w") as file:
            json.dump(data, file, indent=4) # indent=4 formats the data nicely

    # Load method
    def load(self, filename):
        if os.path.exists(filename): # Check if file exists
            with open(filename, "r") as file:
                return json.load(file) # Return the data

class AppManager:
    def __init__(self): # Initialise class attributes.
        self.user = None
        
        
        self.save_manager = SaveManager()
        
        # File names to save to
        self.user_file_name = "user.json"
        self.workout_file_name = "workout.json"
        
        # Application states, 
        # important to keep track of what UI elements to show and when,
        # as well as what events to check for. 
        self.states = {
            "Loading": False,
            "Onboarding": False,
            "Home": False,
            "Exercise Directory Headings": False,
            "Exercise Directory - Arms": False,
            "Exercise Directory - Chest": False,
            "Exercise Directory - Shoulders": False,
            "Exercise Directory - Back": False, 
            "Exercise Directory - Abs": False, 
            "Exercise Directory - Legs": False,
            "User Manual": False,
        }
        
        self.current_elements = []
        
        self._workout = []
    
    # define property "workout"
    @property
    def workout(self):
        return self._workout
    
    # define setter function for workout, 
    # this runs a callback function whenever self.workout is changed
    @workout.setter
    def workout(self, value):
        self._workout = value
        if self.workout_changed_callback:
            self.workout_changed_callback()

    # set_user method
    def set_user(self, age, injuries, disabilities, availability, weight, other_information):
        self.user = User(age, injuries, disabilities, availability, weight, other_information)

    # Method for saving the user
    def save_user(self):
        self.save_manager.save(self.user_file_name, self.user.data)
    
    # Method for loading the user
    def load_user(self):
        # Get the data from the user.json, which is a dictionary, and convert the values to a list
        user_data = self.save_manager.load(self.user_file_name)
        
        if user_data:
            cleaned_user_data = list(user_data.values())
            
            # The * is the unpack operator, 
            # it allows me to pass all the elements in the list as arguments for the user object 
            self.user = User(*cleaned_user_data)
    
    # Methods for saving and loading the workout routine    
    def save_workout(self):
        self.save_manager.save(self.workout_file_name, self.workout)
    
    def load_workout(self):
        workout_data = self.save_manager.load(self.workout_file_name)
        
        if workout_data:
            self.workout = workout_data
    
    # Method for changing the state of the application.
    def change_state(self, new_state: str, elements_to_show: list, elements_to_hide: list):
        # Import within the function to avoid circular import error
        from ui_elements import navigation_icons, workout_icon, workout_generation_icon, exercise_directory_icon, user_manual_icon
        
        # Make sure the new_state parameter is valid,
        # then update the states dictionary.
        if new_state in self.states:
            for state in self.states:
                self.states[state] = False
            self.states[new_state] = True
            
            print(self.states)

            # Show all the neccessary elements
            for element in elements_to_show:
                element.show()
                element.enable()
            
            # Hide all the neccessary elements
            for element in elements_to_hide:
                element.hide()
            
            # Keep track of the new elements to show
            self.current_elements = elements_to_show
            
            # Update navigation icon states based on current state
            if new_state == "Loading":
                for icon in navigation_icons:
                    icon.hide()
                    icon.disable()
            else:
                for icon in navigation_icons:
                    icon.show()
                    icon.enable()
                
                
                if self.states["Onboarding"]:
                    workout_generation_icon.disable()
                elif self.states["Home"]:
                    workout_icon.disable()
                elif self.states["Exercise Directory Headings"]:
                    exercise_directory_icon.disable()
                elif self.states["User Manual"]:
                    user_manual_icon.disable()

        # If the state_to_change_to was invalid, then print "Invalid State", useful for debugging
        else:
            print("Invalid State")


app_manager = AppManager()