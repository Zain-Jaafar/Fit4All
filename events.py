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
    error_notification_label,
)

from utils import app_manager
from ai_model import generate_workout


# Look through the current events and do things accordingly
def handle_events(events: list[pygame.event.Event]):
    for event in events:
        ui_manager.process_events(event) # Handle pygame_gui GUI Events
        
        if app_manager.states["Onboarding"]:
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == onboarding_submit_button:
                    try:
                        age_text = age_input.get_text()
                        
                        try:
                            age = int(age_text)
                        except ValueError:
                            raise ValueError("Age: Please enter a positive integer under 150.")
                        
                        if not(0 < age < 150):
                            raise ValueError("Age: Please enter a positive integer under 150.")
                        
                        injuries = injuries_input.get_text()
                        disabilities = disabilities_input.get_text()
                        
                        availability_text = availability_input.get_text()
                        
                        try:
                            availability = int(availability_text)
                        except:
                            raise ValueError("Please enter a positive integer under 300.")
                        
                        if not(0 < availability < 300):
                            raise ValueError("Please enter a positive integer under 300.")
                        
                        other_information = other_information_input.get_text()
                        
                        
                        app_manager.set_user(age, injuries, disabilities, availability, other_information)
                        app_manager.save_user()
                        
                        
                        workout_generation_thread = threading.Thread(target=generate_workout, args=(app_manager.user.data,))
                        workout_generation_thread.start()
                        
                        for element in onboarding_elements:
                            element.disable()
                    
                    except ValueError as error:
                        print("Please eneter a valid input: ", error)
                        
                        error_notification_label.set_text(f"{error}")
                        
                        if not error_notification_label.visible:
                            error_notification_label.show()
            
        elif app_manager.states["Home"]:
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == back_button:
                    app_manager.change_state("Onboarding", onboarding_elements, home_elements)
                

        if event.type == pygame.QUIT: # If the user pressed the close button on the window
            pygame.quit() # Uninitialise/quit pygame
            sys.exit() # Cleanly close the python program