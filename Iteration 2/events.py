import pygame
import pygame_gui
import sys
import threading

from ui_elements import (
    ui_manager, 
    onboarding_elements,
    home_elements,
    age_input, 
    injuries_input, 
    disabilities_input, 
    availability_input, 
    other_information_input, 
    onboarding_submit_button, 
    back_button,
    error_notification_heading_label,
    error_notification_label,
)

from utils import app_manager
from ai_model import generate_workout


# Look through the current events and do things accordingly
def handle_events(events: list[pygame.event.Event]):
    for event in events:
        ui_manager.process_events(event) # Handle pygame_gui GUI Events
        
        if app_manager.states["Onboarding"]: # If the user is in the onboarding page
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == onboarding_submit_button: # If the user pressed the submit button
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
                        
                        # Get injuries and disabilities information
                        injuries = injuries_input.get_text()
                        disabilities = disabilities_input.get_text()
                        
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
                        app_manager.set_user(age, injuries, disabilities, availability, other_information)
                        app_manager.save_user()
                        
                        # Run the `generate_workout()` function in a seperate 
                        # thread to prevent blocking the main thread and causing the application to stop responding 
                        workout_generation_thread = threading.Thread(target=generate_workout, args=(app_manager.user.data,))
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
        
        # If the user is in the Home page
        elif app_manager.states["Home"]:
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == back_button: # If the back button is pressed, move the user back to the onboarding page
                    app_manager.change_state("Onboarding", onboarding_elements, home_elements)
                

        if event.type == pygame.QUIT: # If the user pressed the close button on the window
            pygame.quit() # Uninitialise/quit pygame
            sys.exit() # Cleanly close the python program
        