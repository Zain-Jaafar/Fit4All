# This file is where I check for events like mouse clicks, keyboard presses, button clicks, etc. to perform various actions, 
# the main action occuring is triggering the AI workout routine generation.

import pygame
import pygame_gui
import sys
import threading
import random

from ui_elements import (
    ui_manager, 
    workout_generation_form_elements,
    age_input, 
    injuries_input, 
    disabilities_input, 
    availability_input, 
    weight_input,
    other_information_input, 
    workout_generation_form_submit_button, 
    age_error_label,
    availability_error_label,
    loading_label,
    quotes,
    exercise_directory_headings_elements,
    chest_directory_button,
    chest_exercises_elements,
    arms_directory_button,
    arms_exercises_elements,
    shoulders_directory_button,
    shoulders_exercises_elements,
    back_directory_button,
    back_exercises_elements,
    abs_directory_button,
    abs_exercises_elements,
    legs_directory_button,
    legs_exercises_elements,
    exercise_directory_icon,
    workout_icon,
    workout_generation_icon,
    user_manual_icon,
)

from utils import app_manager
from ai_model import generate_workout


# Dictionary to map exercise directory pages to their corresponding ui elements
EXERCISE_PAGES = {
    "Exercise Directory - Arms": [arms_directory_button, arms_exercises_elements],
    "Exercise Directory - Chest": [chest_directory_button, chest_exercises_elements],
    "Exercise Directory - Shoulders": [shoulders_directory_button, shoulders_exercises_elements],
    "Exercise Directory - Back": [back_directory_button, back_exercises_elements],
    "Exercise Directory - Abs": [abs_directory_button, abs_exercises_elements],
    "Exercise Directory - Legs": [legs_directory_button, legs_exercises_elements]
}

INPUT_FIELDS = [
    age_input,
    injuries_input, 
    disabilities_input,
    availability_input,
    weight_input,
    other_information_input
]

def unfocus_all_inputs():
    for input_field in INPUT_FIELDS:
        input_field.unfocus()

# Look through the current events and do things accordingly
def handle_events(events: list[pygame.event.Event]):
    for event in events:
        ui_manager.process_events(event) # Handle pygame_gui GUI Events
        
        # Mouse click event check
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = event.pos
            if event.button == 1:  # Left mouse button
                # First check if we clicked on any input field
                for input_field in INPUT_FIELDS:
                    if input_field.rect.collidepoint(mouse_position):
                        unfocus_all_inputs()  # Unfocus all inputs first
                        input_field.focus()   # Focus the clicked input
                        break
                
                # If user clicks exercise directory icon
                if exercise_directory_icon.rect.collidepoint(mouse_position): 
                    exercise_directory_icon.on_click()
                    workout_icon.enable()
                    exercise_directory_icon.disable()
                    workout_generation_icon.enable()
                    user_manual_icon.enable()
                
                # If user clicks workout generation icon
                elif workout_icon.rect.collidepoint(mouse_position): 
                    workout_icon.on_click()
                    workout_icon.disable()
                    exercise_directory_icon.enable()
                    workout_generation_icon.enable()
                    user_manual_icon.enable()
                    
                # If user clicks workout icon
                elif workout_generation_icon.rect.collidepoint(mouse_position): 
                    workout_generation_icon.on_click()
                    workout_icon.enable()
                    exercise_directory_icon.enable()
                    workout_generation_icon.disable()
                    user_manual_icon.enable()
                
                # If user clicks user manual icon
                elif user_manual_icon.rect.collidepoint(mouse_position): 
                    user_manual_icon.on_click()
                    workout_icon.enable()
                    exercise_directory_icon.enable()
                    workout_generation_icon.enable()
                    user_manual_icon.disable()
        
        # Listen for if the user presses a keyboard button
        if event.type == pygame.KEYDOWN:
            if app_manager.states["Workout Generation Form"]:
                # If the user pressed the TAB button
                if event.key == pygame.K_TAB: 
                    focused_index = -1
                    
                    # Find the index of the currently focused input box
                    for index, input_field in enumerate(INPUT_FIELDS):
                        if input_field.is_focused:
                            focused_index = index
                            break
                    
                    # If shift is held, go backwards, otherwise go forwards
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        next_index = (focused_index - 1) % len(INPUT_FIELDS)
                    else:
                        next_index = (focused_index + 1) % len(INPUT_FIELDS)
                    
                    unfocus_all_inputs()  # Unfocus all inputs first
                    INPUT_FIELDS[next_index].focus()  # Focus the next input

        if event.type == pygame_gui.UI_BUTTON_PRESSED: # Pygame_gui custom event
            # Handle main states
            if app_manager.states["Workout Generation Form"]: # If the user is in the workout generation form page
                if event.ui_element == workout_generation_form_submit_button: # If the user pressed the submit button
                    # Pick a new random quote for the loading screen
                    loading_label.set_text(random.choice(quotes))
                    
                    # Hide the error message labels at first
                    age_error_label.hide()
                    availability_error_label.hide()
                    
                    try:
                        # Get age and ensure it is withing the bounds
                        age_text = age_input.get_text().strip()
                        
                        # Ensure that age is a number and within the boundaries 
                        try:
                            age = int(age_text)
                        except ValueError:
                            raise ValueError("Age", "Please enter a positive integer under 150.")
                        
                        if not(0 < age < 150):
                            raise ValueError("Age", "Please enter a positive integer under 150.")
                        
                        # Get injuries, disabilities, and weight information
                        injuries = injuries_input.get_text()
                        disabilities = disabilities_input.get_text()
                        
                        # Users can use whatever unit they want,
                        # so weight is kept as a string
                        weight = weight_input.get_text() 
                        
                        # Get time availability in minutes and ensure it is within the bounds
                        availability_text = availability_input.get_text()
                        
                        # Ensure that time availability in minutes is a number and within the boundaries
                        try:
                            availability = int(availability_text)
                        except:
                            raise ValueError("Time Availability", "Please enter a positive integer under 300.")
                        
                        if not(0 < availability < 300):
                            raise ValueError("Time Availability", "Please enter a positive integer under 300.")
                        
                        # Get info from the "other information" input box
                        other_information = other_information_input.get_text()
                        
                        # Create the user object in the app_manager class and save its data
                        app_manager.set_user(age, injuries, disabilities, availability, weight, other_information)
                        app_manager.save_user()
                        
                        # Run the `generate_workout()` function in a seperate 
                        # thread to prevent blocking the main thread and causing the application to stop responding 
                        workout_generation_thread = threading.Thread(target=generate_workout, args=(app_manager.user_data,), daemon=True)
                        workout_generation_thread.start()
                        
                        # Disable all the elements in the workout generation form 
                        for element in workout_generation_form_elements:
                            element.disable()
                    
                    # If an error occures
                    except ValueError as error:
                        error_heading = error.args[0]
                        error_message = error.args[1]
                        
                        print("Please eneter a valid input: ", error_heading, error_message)
                        
                        # If there an error was raised, 
                        # set the text of the notification labels to be the error message,
                        if error_heading == "Age":
                            age_error_label.set_text(f"{error_message}")
                            
                            # Show the notification label if it is not already shown
                            if not age_error_label.visible:
                                age_error_label.show()
                        elif error_heading == "Time Availability":
                            availability_error_label.set_text(f"{error_message}")
                            
                            # Show the notification label if it is not already shown
                            if not availability_error_label.visible:
                                availability_error_label.show()
                        
        
            elif app_manager.states["Home"]: # If the user is in the Home page
                
                # If the user clicked one of the "Read More" buttons for the exercises,
                # run that exercises' on_button_pressed() function
                for exercise in app_manager.exercise_elements:
                    if exercise.elements['button'] == event.ui_element:
                        exercise.on_button_pressed()
                        break
            
            # If the user is in the exercise directory headings page, 
            # and they click on one of the buttons for a specific muscle group,
            # send them to the page with exercises corresponding to that muscle group
            elif app_manager.states["Exercise Directory Headings"]:
                for key, value in EXERCISE_PAGES.items():
                    exercise_directory_button = value[0]
                    elements_to_show = value[1]
                    
                    if exercise_directory_button:
                        app_manager.change_state(key, elements_to_show, exercise_directory_headings_elements)
                        exercise_directory_icon.enable()
                        break
        

        if event.type == pygame.QUIT: # If the user pressed the close button on the window
            pygame.quit() # Uninitialise/quit pygame
            sys.exit() # Cleanly close the python program
