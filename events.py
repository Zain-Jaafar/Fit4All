import pygame
import pygame_gui
import sys

from ui_management import ui_manager, age_input, injuries_input, disabilities_input, availability_input, other_information_input, onboarding_submit_button
from utils import app_manager, generate_workout


# Look through the current events and do things accordingly
def handle_events(events: list[pygame.event.Event]):
    for event in events:
        ui_manager.process_events(event) # Handle pygame_gui GUI Events
        
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == onboarding_submit_button:
                onboarding_submit_button.disable()
                
                age = age_input.get_text()
                injuries = injuries_input.get_text()
                disabilities = disabilities_input.get_text()
                availability = availability_input.get_text()
                other_information = other_information_input.get_text()
                
                app_manager.set_user(age, injuries, disabilities, availability, other_information)
                app_manager.save_user()
                
                generate_workout(app_manager.user.data)
                

        if event.type == pygame.QUIT: # If the user pressed the close button on the window
            pygame.quit() # Uninitialise/quit pygame
            sys.exit() # Cleanly close the python program