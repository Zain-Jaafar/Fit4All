import pygame
import pygame_gui
import sys
import threading
import random

from ui_elements import (
    ui_manager, 
    onboarding_elements,
    home_elements,
    age_input, 
    injuries_input, 
    disabilities_input, 
    availability_input, 
    weight_input,
    other_information_input, 
    onboarding_submit_button, 
    back_to_onboarding_button,
    error_notification_heading_label,
    error_notification_label,
    loading_label,
    quotes,
    exercise_directory_headings_elements,
    exercise_directory_button,
    home_button,
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
    legs_exercises_elements
)

from utils import app_manager
from ai_model import generate_workout


# Dictionary to map exercise directory pages to their corresponding ui elements
EXERCISE_PAGES = {
    "Exercise Directory - Arms": arms_exercises_elements,
    "Exercise Directory - Chest": chest_exercises_elements,
    "Exercise Directory - Shoulders": shoulders_exercises_elements,
    "Exercise Directory - Back": back_exercises_elements,
    "Exercise Directory - Abs": abs_exercises_elements,
    "Exercise Directory - Legs": legs_exercises_elements
}

# Look through the current events and do things accordingly
def handle_events(events: list[pygame.event.Event]):
    for event in events:
        ui_manager.process_events(event) # Handle pygame_gui GUI Events
        
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            # Handle main states
            if app_manager.states["Onboarding"]: # If the user is in the onboarding page
                if event.ui_element == onboarding_submit_button: # If the user pressed the submit button
                    loading_label.set_text(random.choice(quotes))
                    
                    try:
                        # Get age and ensure it is withing the bounds
                        age_text = age_input.get_text().strip()
                        
                        # Ensure that age is a number and within the boundaries 
                        try:
                            age = int(age_text)
                        except ValueError:
                            raise ValueError("Age:", "Please enter a positive integer under 150.")
                        
                        if not(0 < age < 150):
                            raise ValueError("Age:", "Please enter a positive integer under 150.")
                        
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
                            raise ValueError("Time Availability:", "Please enter a positive integer under 300.")
                        
                        if not(0 < availability < 300):
                            raise ValueError("Time Availability:", "Please enter a positive integer under 300.")
                        
                        # Get info from the "other information" input box
                        other_information = other_information_input.get_text()
                        
                        # Create the user object in the app_manager class and save its data
                        app_manager.set_user(age, injuries, disabilities, availability, weight, other_information)
                        app_manager.save_user()
                        
                        # Run the `generate_workout()` function in a seperate 
                        # thread to prevent blocking the main thread and causing the application to stop responding 
                        workout_generation_thread = threading.Thread(target=generate_workout, args=(app_manager.user.data,), daemon=True)
                        workout_generation_thread.start()
                        
                        # Disable all the elements in the onboarding 
                        for element in onboarding_elements:
                            element.disable()
                    
                    # If an error occures
                    except ValueError as error:
                        error_heading = error.args[0]
                        error_message = error.args[1]
                        
                        print("Please eneter a valid input: ", error_heading, error_message)
                        
                        # If there an error was raised, 
                        # set the text of the notification labels to be the error message,
                        error_notification_heading_label.set_text(f"{error_heading}")
                        error_notification_label.set_text(f"{error_message}")
                        
                        # Show the notification label if it is not already shown
                        if not error_notification_label.visible:
                            error_notification_label.show()
        
            elif app_manager.states["Home"]: # If the user is in the Home page
                if event.ui_element == back_to_onboarding_button: # If the back button is pressed, move the user back to the onboarding page
                    app_manager.change_state("Onboarding", onboarding_elements, home_elements)
                elif event.ui_element == exercise_directory_button: # If exercise directory button is pressed, move the user to the exercise directory
                    app_manager.change_state("Exercise Directory Headings", exercise_directory_headings_elements, home_elements)
            
            # If the user is in the exercise directory headings page, 
            # and they click on one of the buttons for a specific muscle group,
            # send them to the page with exercises corresponding to that muscle group
            elif app_manager.states["Exercise Directory Headings"]:
                if event.ui_element == home_button:
                    app_manager.change_state("Home", home_elements, exercise_directory_headings_elements)
                elif event.ui_element == chest_directory_button:
                    app_manager.change_state("Exercise Directory - Chest", chest_exercises_elements, exercise_directory_headings_elements)
                elif event.ui_element == arms_directory_button:
                    app_manager.change_state("Exercise Directory - Arms", arms_exercises_elements, exercise_directory_headings_elements)
                elif event.ui_element == shoulders_directory_button:
                    app_manager.change_state("Exercise Directory - Shoulders", shoulders_exercises_elements, exercise_directory_headings_elements)
                elif event.ui_element == back_directory_button:
                    app_manager.change_state("Exercise Directory - Back", back_exercises_elements, exercise_directory_headings_elements)
                elif event.ui_element == abs_directory_button:
                    app_manager.change_state("Exercise Directory - Abs", abs_exercises_elements, exercise_directory_headings_elements)
                elif event.ui_element == legs_directory_button:
                    app_manager.change_state("Exercise Directory - Legs", legs_exercises_elements, exercise_directory_headings_elements)
            
            # Generic handler for all exercise directory pages
            else:
                # Check if were in any exercise directory page
                for state, elements in EXERCISE_PAGES.items():
                    if app_manager.states[state]:
                        
                        # the -1 index is the final element in the list, 
                        # which is the position of the back button no matter which 
                        # exercise directory page the user is in
                        back_button = elements[-1] 
                        if event.ui_element == back_button:
                            app_manager.change_state("Exercise Directory Headings", 
                                                   exercise_directory_headings_elements, 
                                                   elements)
                            break

        if event.type == pygame.QUIT: # If the user pressed the close button on the window
            pygame.quit() # Uninitialise/quit pygame
            sys.exit() # Cleanly close the python program
